import { StrictMode, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Dialog } from '@base-ui/react/dialog';
import { mergeProps } from '@base-ui/react/merge-props';
import * as stylex from '@stylexjs/stylex';
import { colors } from './theme.stylex';
import './index.css';

const darkTheme = stylex.createTheme(colors, {
  surface: '#17212b', text: '#ffffff', accent: '#a8c7fa',
});
const styles = stylex.create({
  page: { boxSizing: 'border-box', minHeight: '100vh', padding: 24, backgroundColor: colors.surface, color: colors.text },
  button: {
    paddingBlock: 10, paddingInline: 16, borderRadius: 6,
    borderWidth: 2, borderStyle: 'solid', borderColor: colors.accent,
    backgroundColor: colors.surface, color: colors.text,
    outlineWidth: { default: 0, ':focus-visible': 3 },
    outlineStyle: 'solid', outlineColor: colors.accent, outlineOffset: 3,
  },
  open: { borderBottomWidth: 6 },
  backdrop: { position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.45)' },
  popup: {
    position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
    boxSizing: 'border-box', width: 'min(420px, calc(100vw - 32px))',
    maxHeight: 'calc(100vh - 32px)', overflowY: 'auto',
    padding: 24, borderRadius: 12, backgroundColor: colors.surface, color: colors.text,
  },
  opened: (width: number) => ({ borderWidth: width, borderStyle: 'solid', borderColor: colors.accent }),
  actions: { display: 'flex', flexWrap: 'wrap', gap: 12 },
});

function App() {
  const [dark, setDark] = useState(false);
  const [closeClicks, setCloseClicks] = useState(0);
  const firstControl = useRef<HTMLButtonElement>(null);
  return (
    <main {...stylex.props(styles.page, dark && darkTheme)}>
      <h1>Dialog integration evaluation</h1>
      <output aria-label="Close clicks">{closeClicks}</output>
      <Dialog.Root>
        <Dialog.Trigger className={(state) => stylex.props(styles.button, state.open && styles.open).className}>
          Open settings
        </Dialog.Trigger>
        <Dialog.Portal {...stylex.props(dark && darkTheme)}>
          <Dialog.Backdrop {...stylex.props(styles.backdrop)} />
          <Dialog.Popup
            initialFocus={firstControl}
            render={(baseProps, state) => (
              <section {...mergeProps<'section'>(stylex.props(styles.popup, styles.opened(state.open ? 3 : 0)), baseProps)} />
            )}
          >
            <Dialog.Title>Settings</Dialog.Title>
            <Dialog.Description>Choose the page appearance.</Dialog.Description>
            <div {...stylex.props(styles.actions)}>
              <button ref={firstControl} {...stylex.props(styles.button)} onClick={() => setDark((value) => !value)}>
                Switch to {dark ? 'light' : 'dark'} theme
              </button>
              <Dialog.Close {...stylex.props(styles.button)} onClick={() => setCloseClicks((count) => count + 1)}>
                Close settings
              </Dialog.Close>
            </div>
          </Dialog.Popup>
        </Dialog.Portal>
      </Dialog.Root>
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<StrictMode><App /></StrictMode>);
