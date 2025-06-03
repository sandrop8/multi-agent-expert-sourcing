import './globals.css';

export const metadata = {
  title: 'Expert Sourcing Demo',
  description: 'Connect projects with skilled freelancers through AI-powered matching. Submit projects or join as a freelancer.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className="h-full flex flex-col bg-gradient-to-br from-amber-50 via-orange-50 to-amber-100">
        {children}
      </body>
    </html>
  )
}
