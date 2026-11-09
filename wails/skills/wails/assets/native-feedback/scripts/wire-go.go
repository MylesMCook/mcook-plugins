// wire-go rewrites only the supported Wails construction sites. It never writes files.
package main

import (
	"flag"
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"io"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

type edit struct {
	at     int
	remove int
	value  string
}
type construction struct {
	stmt  *ast.AssignStmt
	call  *ast.CallExpr
	name  string
	fn    *ast.FuncDecl
	block *ast.BlockStmt
}

func main() {
	module := flag.String("module", "", "Wails Go module from go.mod")
	flag.Parse()
	if !regexp.MustCompile(`^[A-Za-z0-9._~/-]+$`).MatchString(*module) || strings.Contains(*module, "..") {
		fail("supply a valid --module from the native go.mod")
	}
	source, err := io.ReadAll(os.Stdin)
	if err != nil {
		fail(err.Error())
	}
	result, err := wire(string(source), *module)
	if err != nil {
		fail(err.Error())
	}
	fmt.Print(result)
}

func fail(message string) { fmt.Fprintln(os.Stderr, "Wails feedback setup:", message); os.Exit(1) }
func wire(source, module string) (string, error) {
	fset := token.NewFileSet()
	file, err := parser.ParseFile(fset, "main.go", source, parser.ParseComments)
	if err != nil {
		return "", fmt.Errorf("fix existing Go syntax first: %w", err)
	}
	offset := func(pos token.Pos) int { return fset.Position(pos).Offset }
	appAlias, osAlias := "", ""
	for _, imp := range file.Imports {
		path, _ := strconv.Unquote(imp.Path.Value)
		alias := ""
		if imp.Name != nil {
			alias = imp.Name.Name
		}
		if path == "github.com/wailsapp/wails/v3/pkg/application" {
			appAlias = "application"
			if alias != "" {
				appAlias = alias
			}
		}
		if path == "os" {
			osAlias = "os"
			if alias != "" {
				osAlias = alias
			}
		}
		if path == module+"/internal/nativefeedback" {
			return "", fmt.Errorf("Go feedback wiring already exists; use the setup receipt to rerun")
		}
	}
	if appAlias == "" || appAlias == "." || appAlias == "_" {
		return "", fmt.Errorf("expected a named Wails v3 application import")
	}
	if osAlias == "." || osAlias == "_" {
		return "", fmt.Errorf("the os import must be named to wire feedback")
	}
	conflict := false
	ast.Inspect(file, func(n ast.Node) bool {
		if ident, ok := n.(*ast.Ident); ok && (ident.Name == "feedbackBridge" || ident.Name == "feedbackErr" || ident.Name == "nativefeedback") {
			conflict = true
		}
		return true
	})
	if conflict {
		return "", fmt.Errorf("feedbackBridge, feedbackErr or nativefeedback is already declared; choose a conflict-free entry")
	}
	var apps []construction
	for _, decl := range file.Decls {
		fn, ok := decl.(*ast.FuncDecl)
		if !ok || fn.Body == nil {
			continue
		}
		ast.Inspect(fn.Body, func(n ast.Node) bool {
			block, ok := n.(*ast.BlockStmt)
			if !ok {
				return true
			}
			for _, statement := range block.List {
				stmt, ok := statement.(*ast.AssignStmt)
				if !ok || len(stmt.Rhs) != 1 || len(stmt.Lhs) != 1 {
					continue
				}
				call, ok := stmt.Rhs[0].(*ast.CallExpr)
				if !ok {
					continue
				}
				selector, ok := call.Fun.(*ast.SelectorExpr)
				if !ok || selector.Sel.Name != "New" {
					continue
				}
				receiver, ok := selector.X.(*ast.Ident)
				if !ok || receiver.Name != appAlias {
					continue
				}
				name, ok := stmt.Lhs[0].(*ast.Ident)
				if !ok || name.Name == "_" {
					continue
				}
				apps = append(apps, construction{stmt, call, name.Name, fn, block})
			}
			return true
		})
	}
	if len(apps) != 1 {
		return "", fmt.Errorf("expected exactly one direct Wails application.New assignment; select its entry file explicitly")
	}
	app := apps[0]
	if len(app.call.Args) != 1 {
		return "", fmt.Errorf("application.New must receive one application.Options literal")
	}
	options, ok := app.call.Args[0].(*ast.CompositeLit)
	if !ok {
		return "", fmt.Errorf("application.New options are indirect; setup requires an application.Options literal")
	}
	typ, ok := options.Type.(*ast.SelectorExpr)
	if !ok || typ.Sel.Name != "Options" {
		return "", fmt.Errorf("application.New must receive an application.Options literal")
	}
	var windows []construction
	for _, statement := range app.block.List {
		stmt, ok := statement.(*ast.AssignStmt)
		if !ok || len(stmt.Rhs) != 1 || len(stmt.Lhs) != 1 {
			continue
		}
		call, ok := stmt.Rhs[0].(*ast.CallExpr)
		if !ok {
			continue
		}
		selector, ok := call.Fun.(*ast.SelectorExpr)
		if !ok || selector.Sel.Name != "NewWithOptions" {
			continue
		}
		holder, ok := selector.X.(*ast.SelectorExpr)
		if !ok || holder.Sel.Name != "Window" {
			continue
		}
		receiver, ok := holder.X.(*ast.Ident)
		if !ok || receiver.Name != app.name {
			continue
		}
		name, ok := stmt.Lhs[0].(*ast.Ident)
		if !ok || name.Name == "_" {
			continue
		}
		windows = append(windows, construction{stmt, call, name.Name, app.fn, app.block})
	}
	var mainWindows []construction
	for _, window := range windows {
		if len(window.call.Args) != 1 {
			continue
		}
		opts, ok := window.call.Args[0].(*ast.CompositeLit)
		if !ok {
			continue
		}
		for _, elt := range opts.Elts {
			pair, ok := elt.(*ast.KeyValueExpr)
			if !ok {
				continue
			}
			key, ok := pair.Key.(*ast.Ident)
			if !ok || key.Name != "Name" {
				continue
			}
			name, ok := pair.Value.(*ast.BasicLit)
			if !ok {
				continue
			}
			value, _ := strconv.Unquote(name.Value)
			if value == "main" {
				mainWindows = append(mainWindows, window)
			}
		}
	}
	if len(mainWindows) == 1 {
		windows = mainWindows
	}
	if len(windows) != 1 || windows[0].stmt.Pos() < app.stmt.End() {
		return "", fmt.Errorf("expected exactly one trusted main window after application.New; name it main to disambiguate")
	}
	window := windows[0]
	changes := []edit{}
	imports := []string{`"` + module + `/internal/nativefeedback"`}
	if osAlias == "" {
		osAlias = "os"
		imports = append(imports, `"os"`)
	}
	importAdded := false
	for _, decl := range file.Decls {
		group, ok := decl.(*ast.GenDecl)
		if !ok || group.Tok != token.IMPORT || !group.Lparen.IsValid() {
			continue
		}
		changes = append(changes, edit{offset(group.Rparen), 0, "\t" + strings.Join(imports, "\n\t") + "\n"})
		importAdded = true
		break
	}
	if !importAdded {
		changes = append(changes, edit{offset(file.Name.End()), 0, "\n\nimport (\n\t" + strings.Join(imports, "\n\t") + "\n)"})
	}
	pos := offset(app.stmt.Pos())
	lineStart := strings.LastIndex(source[:pos], "\n") + 1
	indent := source[lineStart:pos]
	if strings.TrimSpace(indent) != "" {
		return "", fmt.Errorf("application.New must start on its own line")
	}
	failure := "panic(feedbackErr)"
	if app.fn.Type.Results != nil && len(app.fn.Type.Results.List) == 1 {
		if ident, ok := app.fn.Type.Results.List[0].Type.(*ast.Ident); ok && ident.Name == "error" {
			failure = "return feedbackErr"
		} else {
			return "", fmt.Errorf("application entry must return error or no result")
		}
	} else if app.fn.Type.Results != nil && len(app.fn.Type.Results.List) > 0 {
		return "", fmt.Errorf("application entry must return error or no result")
	}
	start := "feedbackBridge, feedbackErr := nativefeedback.Start(nativefeedback.Config{CompanionURL: " + osAlias + ".Getenv(\"WAILS_FEEDBACK_COMPANION_URL\")})\n" + indent + "if feedbackErr != nil {\n" + indent + "\t" + failure + "\n" + indent + "}\n" + indent + "defer nativefeedback.Stop(feedbackBridge)\n" + indent
	changes = append(changes, edit{pos, 0, start})
	services := 0
	for _, elt := range options.Elts {
		pair, ok := elt.(*ast.KeyValueExpr)
		if !ok {
			return "", fmt.Errorf("application.Options must use named fields")
		}
		key, ok := pair.Key.(*ast.Ident)
		if !ok {
			continue
		}
		if key.Name == "SingleInstance" {
			if ident, ok := pair.Value.(*ast.Ident); ok && ident.Name == "nil" {
				continue
			}
			value := pair.Value
			if pointer, ok := value.(*ast.UnaryExpr); ok && pointer.Op == token.AND {
				value = pointer.X
			}
			instance, ok := value.(*ast.CompositeLit)
			if !ok {
				return "", fmt.Errorf("SingleInstance options are indirect; use a literal to preserve isolated development launches")
			}
			identities := 0
			for _, field := range instance.Elts {
				property, ok := field.(*ast.KeyValueExpr)
				if !ok {
					return "", fmt.Errorf("SingleInstance options must use named fields")
				}
				name, ok := property.Key.(*ast.Ident)
				if !ok || name.Name != "UniqueID" {
					continue
				}
				identities++
				begin, end := offset(property.Value.Pos()), offset(property.Value.End())
				changes = append(changes, edit{begin, end - begin, "nativefeedback.InstanceID(feedbackBridge, " + source[begin:end] + ")"})
			}
			if identities != 1 {
				return "", fmt.Errorf("SingleInstance must have one UniqueID to preserve isolated development launches")
			}
			continue
		}
		if key.Name != "Services" {
			continue
		}
		services++
		begin, end := offset(pair.Value.Pos()), offset(pair.Value.End())
		changes = append(changes, edit{begin, end - begin, "nativefeedback.Services(feedbackBridge, " + source[begin:end] + ")"})
	}
	if services > 1 {
		return "", fmt.Errorf("application.Options repeats Services")
	}
	if services == 0 {
		changes = append(changes, edit{offset(options.Lbrace) + 1, 0, "\n" + indent + "\tServices: nativefeedback.Services(feedbackBridge, nil),"})
	}
	changes = append(changes, edit{offset(window.stmt.End()), 0, "\n" + indent + "nativefeedback.Attach(feedbackBridge, " + window.name + ")"})
	sort.SliceStable(changes, func(i, j int) bool { return changes[i].at > changes[j].at })
	for _, change := range changes {
		source = source[:change.at] + change.value + source[change.at+change.remove:]
	}
	if _, err = parser.ParseFile(token.NewFileSet(), "wired.go", source, 0); err != nil {
		return "", fmt.Errorf("generated wiring could not be parsed: %w", err)
	}
	return source, nil
}
