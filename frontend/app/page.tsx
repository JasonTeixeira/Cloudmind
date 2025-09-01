import { redirect } from 'next/navigation'

export default function HomePage() {
  // Redirect to dashboard immediately to show our cyberpunk UI
  redirect('/dashboard')
}