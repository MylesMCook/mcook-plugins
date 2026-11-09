import { Agentation } from "agentation";

export default function FeedbackOverlay({ endpoint }: { endpoint: string }) {
  return <Agentation appName={WAILS_FEEDBACK_APP_NAME} endpoint={endpoint} />;
}
