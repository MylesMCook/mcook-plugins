export async function completeOnboarding(profile) {
  return fetch("https://api.example.invalid/onboarding", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      ...profile,
      effects: ["email", "billing-customer", "publish-profile", "sync-job"]
    })
  });
}
