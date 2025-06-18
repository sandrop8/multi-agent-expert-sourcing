# React Frontend Architecture & Best Practices Guide

This document provides comprehensive best practices for React/Next.js development, focusing on TypeScript integration, component architecture, and project structure that can be followed for consistent development across projects.

## 🏗️ **Project Architecture Overview**

### **Recommended File Structure**
```
project-name/
├── README.md                     # Project overview and quick start
├── package.json                  # Dependencies and scripts
├── next.config.js               # Next.js configuration
├── tailwind.config.js           # Tailwind CSS configuration
├── tsconfig.json                # TypeScript configuration
├── .eslintrc.json              # ESLint configuration
├── jest.config.js              # Jest testing configuration
├── playwright.config.ts        # Playwright E2E testing
├── Makefile                    # Development commands
├── .env.local                  # Environment variables (local)
├── .env.example               # Environment variables template
├── app/                       # Next.js App Router (Next.js 13+)
│   ├── globals.css           # Global styles
│   ├── layout.tsx            # Root layout component
│   ├── page.tsx              # Homepage component
│   ├── loading.tsx           # Global loading UI
│   ├── error.tsx             # Global error UI
│   ├── not-found.tsx         # 404 page
│   ├── (routes)/             # Route groups (optional)
│   ├── api/                  # API routes
│   │   ├── auth/
│   │   ├── users/
│   │   └── health/
│   ├── dashboard/            # Dashboard pages
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── loading.tsx
│   ├── profile/              # User profile pages
│   │   ├── page.tsx
│   │   ├── edit/
│   │   └── settings/
│   └── auth/                 # Authentication pages
│       ├── login/
│       ├── register/
│       └── reset-password/
├── components/               # Reusable UI components
│   ├── ui/                  # Base UI components (shadcn/ui style)
│   │   ├── __tests__/      # Component-specific tests
│   │   │   ├── button.test.tsx
│   │   │   └── card.test.tsx
│   │   ├── button.tsx      # Button component
│   │   ├── card.tsx        # Card component
│   │   ├── input.tsx       # Input component
│   │   ├── modal.tsx       # Modal component
│   │   └── index.ts        # Barrel exports
│   ├── forms/              # Form components
│   │   ├── LoginForm.tsx
│   │   ├── ProfileForm.tsx
│   │   └── ContactForm.tsx
│   ├── layout/             # Layout components
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Sidebar.tsx
│   │   └── Navigation.tsx
│   ├── features/           # Feature-specific components
│   │   ├── auth/
│   │   │   ├── AuthProvider.tsx
│   │   │   ├── LoginButton.tsx
│   │   │   └── UserProfile.tsx
│   │   ├── dashboard/
│   │   │   ├── DashboardCard.tsx
│   │   │   └── MetricsChart.tsx
│   │   └── chat/
│   │       ├── ChatMessage.tsx
│   │       ├── ChatInput.tsx
│   │       └── MessageList.tsx
│   └── common/             # Common/shared components
│       ├── LoadingSpinner.tsx
│       ├── ErrorBoundary.tsx
│       └── PageTitle.tsx
├── hooks/                  # Custom React hooks
│   ├── useAuth.ts         # Authentication hook
│   ├── useLocalStorage.ts # Local storage hook
│   ├── useApi.ts          # API interaction hook
│   ├── useDebounce.ts     # Debounce hook
│   └── index.ts           # Barrel exports
├── lib/                   # Utility libraries and configurations
│   ├── utils.ts          # Utility functions
│   ├── constants.ts      # Application constants
│   ├── validations.ts    # Form validation schemas
│   ├── api.ts            # API client configuration
│   ├── auth.ts           # Authentication utilities
│   └── db.ts             # Database client (if applicable)
├── types/                # TypeScript type definitions
│   ├── index.ts          # Common types
│   ├── api.ts            # API response types
│   ├── auth.ts           # Authentication types
│   ├── user.ts           # User-related types
│   └── jest-dom.d.ts     # Testing type extensions
├── styles/               # Styling files
│   ├── globals.css       # Global styles (if not in app/)
│   ├── components.css    # Component-specific styles
│   └── utilities.css     # Utility classes
├── public/               # Static assets
│   ├── images/          # Image assets
│   │   ├── logo.svg
│   │   ├── hero-bg.jpg
│   │   └── office/      # Organized by category
│   │       ├── office1.png
│   │       ├── office2.png
│   │       └── office3.png
│   ├── icons/           # Icon assets
│   │   ├── favicon.ico
│   │   └── apple-touch-icon.png
│   ├── fonts/           # Custom fonts (if not using web fonts)
│   └── docs/            # Documentation assets
│       ├── api-diagram.png
│       └── architecture.png
├── __tests__/           # Global test utilities and setup
│   ├── setup.ts         # Test setup configuration
│   ├── mocks/           # Test mocks
│   │   ├── api.ts
│   │   └── router.ts
│   └── utils/           # Test utilities
│       ├── render.tsx   # Custom render function
│       └── fixtures.ts  # Test data fixtures
├── e2e/                 # End-to-end tests
│   ├── auth.spec.ts     # Authentication E2E tests
│   ├── dashboard.spec.ts # Dashboard E2E tests
│   └── user-flow.spec.ts # Complete user flow tests
├── docs/                # Project documentation
│   ├── COMPONENT_GUIDE.md      # Component development guide
│   ├── TESTING_STRATEGY.md     # Testing approach and patterns
│   ├── DEPLOYMENT.md           # Deployment instructions
│   └── STYLING_GUIDE.md        # Styling conventions
└── coverage/            # Test coverage reports (generated)
    ├── lcov-report/
    └── coverage-final.json

> ⚠️ **Barrel-file Caveats**
> We use `index.ts` barrel files for cleaner imports, but they must be used thoughtfully:
> -   **Avoid `export *`**: Prefer explicit named exports (`export { Button } from './Button'`). This makes the dependency graph clearer and helps bundlers with tree-shaking.
> -   **Watch for Circular Dependencies**: Never have two barrels import from each other. Our ESLint configuration (`import/no-cycle`) is enabled to catch these mistakes automatically.
> -   **Keep Barrels Shallow**: A barrel file should only export modules from its own directory. Avoid creating barrels that re-export other barrels from deeper in the file tree.

## 🧩 **Component Architecture Principles**

### **1. Component Organization Patterns**

#### **By Feature vs. By Type**
```typescript
// ✅ PREFERRED - Feature-based organization
components/
├── features/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── AuthProvider.tsx
│   │   └── useAuth.ts        # Co-locate related hooks
│   ├── dashboard/
│   │   ├── DashboardCard.tsx
│   │   ├── MetricsChart.tsx
│   │   └── useDashboard.ts
│   └── chat/
│       ├── ChatMessage.tsx
│       ├── ChatInput.tsx
│       └── types.ts          # Feature-specific types

// ❌ AVOID - Type-based organization (for complex features)
components/
├── forms/
│   ├── LoginForm.tsx
│   ├── DashboardForm.tsx
│   └── ChatForm.tsx          # Mixed concerns
├── cards/
│   ├── UserCard.tsx
│   ├── DashboardCard.tsx
│   └── ChatCard.tsx
```

#### **Component Hierarchy**
```typescript
// Base UI components (atomic)
components/ui/Button.tsx
components/ui/Input.tsx
components/ui/Card.tsx

// Composite components (molecular)
components/forms/LoginForm.tsx
components/cards/UserCard.tsx

// Feature components (organisms)
components/features/auth/AuthProvider.tsx
components/layout/Header.tsx

// Page-level components (templates)
app/dashboard/page.tsx
app/profile/page.tsx
```

### **2. TypeScript Component Patterns**

#### **Functional Components with Props Interface**
```typescript
// components/ui/Button.tsx
import { ButtonHTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  loading?: boolean
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'default', loading, children, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={loading || props.disabled}
        {...props}
      >
        {loading ? <LoadingSpinner /> : children}
      </button>
    )
  }
)
Button.displayName = 'Button'

export { Button, type ButtonProps }
```

#### **Complex Component with Hooks**
```typescript
// components/features/auth/LoginForm.tsx
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { loginSchema, type LoginFormData } from '@/lib/validations'
import { useAuth } from '@/hooks/useAuth'

interface LoginFormProps {
  redirectTo?: string
  className?: string
}

export function LoginForm({ redirectTo = '/dashboard', className }: LoginFormProps) {
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()
  const { login } = useAuth()

  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  })

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true)
    try {
      await login(data)
      router.push(redirectTo)
    } catch (error) {
      form.setError('root', { message: 'Invalid credentials' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className={className}>
      {/* Form fields */}
    </form>
  )
}
```

## 🎨 **Styling Architecture (Tailwind CSS)**

### **1. Tailwind Configuration**
```javascript
// tailwind.config.js
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}
```

### **2. CSS Variable System**
```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary text-primary-foreground hover:bg-primary/90;
  }
}
```

### **3. Component Variant Patterns**
```typescript
// lib/utils.ts - Using class-variance-authority
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { cva, type VariantProps } from 'class-variance-authority'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'underline-offset-4 hover:underline text-primary',
      },
      size: {
        default: 'h-10 py-2 px-4',
        sm: 'h-9 px-3 rounded-md',
        lg: 'h-11 px-8 rounded-md',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)
```

## 🪝 **Custom Hooks Architecture**

### **1. API Layer Architecture**

A robust API layer is crucial for a scalable frontend. Instead of using `fetch` directly in component-level hooks, we centralize our API client configuration. This provides several key benefits:

-   **Centralized Configuration**: Avoids duplicating base URLs, headers, and timeouts in every call.
-   **Painless Authentication & Logging**: An Axios/Ky instance with interceptors lets you inject auth tokens (and refresh them on 401s) or log errors in one place.
-   **Consistent Error Handling**: A single client makes it easy to surface consistent toast notifications or Sentry reports.
-   **Cleaner Hooks**: It separates the UI logic from the network transport details.

#### **API Client Example**
```typescript
// lib/api.ts - Example Centralized API Client
import axios from 'axios'

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add a request interceptor to inject the auth token
apiClient.interceptors.request.use(async (config) => {
  // Logic to get the token, e.g., from localStorage or a cookie
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Optional: Add a response interceptor for global error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle global errors, e.g., show a toast notification
    if (error.response.status === 401) {
      // Handle token refresh or redirect to login
    }
    return Promise.reject(error)
  }
)

export default apiClient
```

#### **Data Fetching Hook Example**
```typescript
// hooks/useApi.ts - Refactored to use the client
import { useState, useEffect, useCallback } from 'react'
import apiClient from '@/lib/api' // Import the centralized client
import { AxiosError, AxiosRequestConfig } from 'axios'

interface UseApiResult<T> {
  data: T | null
  loading: boolean
  error: AxiosError | null
  refetch: () => void
}

export function useApi<T>(url: string, options?: AxiosRequestConfig): UseApiResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<AxiosError | null>(null)

  const fetchData = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await apiClient.get<T>(url, options)
      setData(response.data)
    } catch (err) {
      setError(err as AxiosError)
    } finally {
      setLoading(false)
    }
  }, [url, options]) // options should be memoized if it's an object

  useEffect(() => {
    fetchData()
  }, [fetchData])

  return { data, loading, error, refetch: fetchData }
}
```

### **2. Authentication Hook**
```typescript
// hooks/useAuth.ts
import { createContext, useContext, useState, useEffect } from 'react'

interface User {
  id: string
  email: string
  name: string
}

interface AuthContextType {
  user: User | null
  login: (credentials: LoginCredentials) => Promise<void>
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
```

## 🗄️ **State Management Architecture**

While React Context is excellent for simple, infrequently updated global data (like theme or user authentication status), a more robust solution is needed for complex, frequently-mutating, or cross-feature state.

For these scenarios, **we use [Zustand](https://github.com/pmndrs/zustand) by default**. It offers a simple API with minimal boilerplate, while providing performance-optimized, selective subscriptions out of the box. Redux Toolkit remains a viable option for applications requiring advanced features like time-travel debugging or complex middleware.

### **State Management Options Compared**

#### **1. React Context**
-   **Pros**: Built-in, no extra dependencies.
-   **Use Case**: Great for infrequently changing global data like UI theme, authentication status, or locale.
-   **Caveat**: Every component consuming the context re-renders on each state change. Performance can degrade without careful memoization or splitting data across multiple providers.

#### **2. Zustand**
-   **Pros**: Minimal boilerplate (one-line store setup), no `<Provider>` wrapper needed, and selective subscriptions to prevent unnecessary re-renders.
-   **Use Case**: The default choice for medium-to-large state graphs and performance-sensitive applications where a minimal API is valued.
-   **Cons**: Smaller ecosystem than Redux; middleware for persistence or async thunks must be wired up manually.

#### **3. Redux Toolkit (RTK)**
-   **Pros**: Excellent DevTools with time-travel debugging, extensive middleware support, and a large community.
-   **Use Case**: Ideal for applications that require strict predictability, auditable state changes, cross-tab synchronization, or manage very large, normalized datasets.
-   **Cons**: Involves more boilerplate (actions, reducers, slices); enforces immutability and pure functions, which adds a learning curve.

## 🧪 **Testing Architecture**

### **1. Component Testing Setup**
```typescript
// __tests__/setup.ts
import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

afterEach(() => {
  cleanup()
})
```

### **2. Custom Render Utility**
```typescript
// __tests__/utils/render.tsx
import { ReactElement } from 'react'
import { render, RenderOptions } from '@testing-library/react'
import { AuthProvider } from '@/components/features/auth/AuthProvider'

const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  )
}

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) => render(ui, { wrapper: AllTheProviders, ...options })

export * from '@testing-library/react'
export { customRender as render }
```

### **3. Component Test Patterns**
```typescript
// components/ui/__tests__/Button.test.tsx
import { render, screen } from '@/__tests__/utils/render'
import { Button } from '../Button'

describe('Button', () => {
  it('renders with default props', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument()
  })

  it('applies variant classes correctly', () => {
    render(<Button variant="destructive">Delete</Button>)
    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-destructive')
  })

  it('shows loading state', () => {
    render(<Button loading>Loading</Button>)
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument()
  })
})
```

## 🛠️ **Development Workflow**

### **1. Package.json Scripts**
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:headed": "playwright test --headed",
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

### **2. Environment Configuration**
```bash
# .env.example
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME="My App"
NEXTAUTH_SECRET=your-secret-here
NEXTAUTH_URL=http://localhost:3000
```

### **3. TypeScript Configuration**
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"],
      "@/components/*": ["./components/*"],
      "@/hooks/*": ["./hooks/*"],
      "@/lib/*": ["./lib/*"],
      "@/types/*": ["./types/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## 📋 **Best Practices Checklist**

### **✅ React/Next.js Development Checklist**
- [ ] Use TypeScript for all components and utilities
- [ ] Implement proper component prop interfaces
- [ ] Follow the feature-based folder organization
- [ ] Use Tailwind CSS with consistent design system
- [ ] Implement custom hooks for shared logic
- [ ] Write tests for components and hooks
- [ ] Use proper error boundaries
- [ ] Implement loading states consistently
- [ ] Follow naming conventions (PascalCase for components, camelCase for functions)
- [ ] Use barrel exports (index.ts files) for clean imports
- [ ] Implement proper accessibility (a11y) practices
- [ ] Use Next.js App Router patterns
- [ ] Optimize images with Next.js Image component
- [ ] Implement proper SEO with metadata
- [ ] Use environment variables for configuration

### **✅ Code Quality Standards**
- [ ] ESLint configuration for consistent code style
- [ ] Prettier for automatic code formatting
- [ ] Husky for git hooks
- [ ] TypeScript strict mode enabled
- [ ] Jest and React Testing Library for unit tests
- [ ] Playwright for end-to-end testing
- [ ] Component documentation with JSDoc
- [ ] Consistent naming conventions
- [ ] Proper error handling and user feedback
- [ ] Performance optimization (lazy loading, memoization)

---

## 🎯 **Key Benefits of This Architecture**

1. **Scalability**: Feature-based organization scales well with team size
2. **Type Safety**: Full TypeScript integration prevents runtime errors
3. **Maintainability**: Clear separation of concerns and consistent patterns
4. **Developer Experience**: Excellent tooling and development workflow
5. **Testing**: Comprehensive testing strategy from unit to E2E
6. **Performance**: Next.js optimizations and modern React patterns
7. **Reusability**: Generic patterns that work across projects

This architecture provides a robust, maintainable foundation for React/Next.js applications with TypeScript, ensuring consistent development practices and high code quality across projects.
