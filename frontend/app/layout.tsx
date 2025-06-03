import './globals.css';

export const metadata = {
  title: 'Multi Agent Chat',
  description: 'A modern chat interface for multi-agent interactions.',
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
