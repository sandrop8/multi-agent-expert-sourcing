import './globals.css';

export const metadata = {
  title: 'Expert Sourcing Platform',
  description: 'Connect projects with skilled freelancers through AI-powered matching. Submit projects or join as a freelancer.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className="h-full flex flex-col bg-gray-500">
        {children}
      </body>
    </html>
  )
}
