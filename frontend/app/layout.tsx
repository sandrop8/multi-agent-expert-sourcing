import './globals.css'

export const metadata = {
  title: 'Multi-Agent Expert Sourcing',
  description: 'AI-powered homework assistance with AG-UI protocol integration',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  )
}
