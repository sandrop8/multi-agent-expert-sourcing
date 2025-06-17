# GraphQL API Design Principles

**Comprehensive guide for designing and implementing GraphQL APIs following official GraphQL Foundation best practices.**

> 📖 **Usage**: This document serves as a generic guide for GraphQL API development that can be applied to any project requiring GraphQL API design.
> 🌐 **Source**: Based on [GraphQL Best Practices](https://graphql.org/learn/best-practices/) from the GraphQL Foundation.

---

## 🎯 **Core GraphQL Principles**

### **1. Thinking in Graphs**
- **Model your business domain as a graph**: Design your schema around relationships between entities
- **Nodes and edges**: Think of data as interconnected nodes with relationships (edges)
- **Single graph**: One unified graph that represents your entire data model
- **Client-driven**: Let clients specify exactly what data they need

### **2. Strong Type System**
- **Schema-first development**: Define your schema before implementation
- **Static validation**: Queries are validated against the schema at build time
- **Self-documenting**: Schema serves as the API documentation
- **Evolution without versioning**: Add new fields and types without breaking existing clients

### **3. Single Endpoint**
- **One URL**: All GraphQL operations go through a single endpoint
- **HTTP POST**: Typically use POST method for all operations
- **Introspection**: Schema is discoverable through introspection queries
- **Unified interface**: Single point of entry for all data requirements

---

## 🏗️ **Schema Design Principles**

### **Designing for Clients**
```graphql
# ✅ GOOD - Client-friendly field names
type User {
  id: ID!
  displayName: String!
  profileImageUrl: String
  isActive: Boolean!
}

# ❌ BAD - Database-centric naming
type User {
  user_id: String!
  fname: String!
  img_url: String
  active_flag: Int!
}
```

### **Nullable vs Non-Nullable Fields**
```graphql
type User {
  id: ID!              # Always present - non-nullable
  email: String!       # Required field - non-nullable
  displayName: String  # Optional field - nullable
  posts: [Post!]!      # Non-null list of non-null items
}
```

### **Connection Pattern for Lists**
```graphql
type User {
  posts(first: Int, after: String): PostConnection!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

---

## 🔍 **Query Design Patterns**

### **Field Selection**
```graphql
# Clients specify exactly what they need
query GetUser($id: ID!) {
  user(id: $id) {
    id
    displayName
    email
    posts(first: 10) {
      edges {
        node {
          id
          title
          publishedAt
        }
      }
    }
  }
}
```

### **Nested Queries**
```graphql
# Deep nesting with relationship traversal
query GetPostWithAuthorAndComments($postId: ID!) {
  post(id: $postId) {
    id
    title
    content
    author {
      id
      displayName
      profileImageUrl
    }
    comments(first: 20) {
      edges {
        node {
          id
          content
          author {
            id
            displayName
          }
        }
      }
    }
  }
}
```

### **Query Variables**
```graphql
# Use variables for dynamic values
query GetPosts($status: PostStatus!, $limit: Int = 10) {
  posts(status: $status, first: $limit) {
    edges {
      node {
        id
        title
        status
      }
    }
  }
}
```

---

## ✏️ **Mutation Design Patterns**

### **Input Types**
```graphql
# Define specific input types for mutations
input CreatePostInput {
  title: String!
  content: String!
  tags: [String!]
  publishedAt: DateTime
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
}

type CreatePostPayload {
  post: Post
  errors: [UserError!]!
  success: Boolean!
}
```

### **Error Handling in Mutations**
```graphql
type UserError {
  field: String
  message: String!
  code: String!
}

type CreatePostPayload {
  post: Post
  errors: [UserError!]!
  success: Boolean!
}
```

### **Optimistic Updates**
```graphql
# Include client-side mutation ID for optimistic updates
input CreatePostInput {
  clientMutationId: String
  title: String!
  content: String!
}

type CreatePostPayload {
  clientMutationId: String
  post: Post
  errors: [UserError!]!
}
```

---

## 🔄 **Subscription Design Patterns**

### **Real-time Updates**
```graphql
type Subscription {
  postUpdated(id: ID!): Post!
  commentAdded(postId: ID!): Comment!
  userOnlineStatus(userId: ID!): UserOnlineStatus!
}

# Client subscription
subscription WatchPost($postId: ID!) {
  postUpdated(id: $postId) {
    id
    title
    content
    lastModified
  }
}
```

### **Filtered Subscriptions**
```graphql
type Subscription {
  ordersUpdated(status: OrderStatus): Order!
  notificationsReceived(userId: ID!, types: [NotificationType!]): Notification!
}
```

---

## 🌐 **Serving GraphQL over HTTP**

### **Endpoint Configuration**
```http
# Standard GraphQL endpoint
POST /graphql HTTP/1.1
Content-Type: application/json

{
  "query": "query GetUser($id: ID!) { user(id: $id) { id name } }",
  "variables": { "id": "123" },
  "operationName": "GetUser"
}
```

### **HTTP Status Codes**
- **200 OK**: Successful request (even with GraphQL errors)
- **400 Bad Request**: Malformed GraphQL query
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **405 Method Not Allowed**: Only POST, GET (for introspection) allowed
- **500 Internal Server Error**: Server-side errors

### **Response Format**
```json
{
  "data": {
    "user": {
      "id": "123",
      "name": "John Doe"
    }
  },
  "errors": [
    {
      "message": "Field 'invalidField' not found",
      "locations": [{ "line": 2, "column": 5 }],
      "path": ["user", "invalidField"]
    }
  ],
  "extensions": {
    "tracing": {
      "execution": {
        "duration": 156000
      }
    }
  }
}
```

---

## 🔐 **Authorization Patterns**

### **Field-Level Authorization**
```graphql
type User {
  id: ID!
  displayName: String!
  email: String!     # Only visible to user themselves or admins
  privateNotes: String # Only visible to admins
}
```

### **Context-Based Authorization**
```javascript
// Resolver implementation
const resolvers = {
  User: {
    email: (user, args, context) => {
      if (context.user.id === user.id || context.user.role === 'admin') {
        return user.email;
      }
      throw new AuthenticationError('Insufficient permissions');
    }
  }
};
```

### **Business Logic Layer**
```graphql
# Delegate authorization to business logic layer
type Query {
  user(id: ID!): User
  posts(authorId: ID, published: Boolean): [Post!]!
}

# Business logic handles permissions
# GraphQL layer stays thin and focused on data shape
```

---

## 📄 **Pagination Strategies**

### **Cursor-Based Pagination (Recommended)**
```graphql
type Query {
  posts(first: Int, after: String, last: Int, before: String): PostConnection!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int
}

type PostEdge {
  cursor: String!
  node: Post!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### **Offset-Based Pagination**
```graphql
type Query {
  posts(limit: Int = 20, offset: Int = 0): PostList!
}

type PostList {
  posts: [Post!]!
  totalCount: Int!
  hasMore: Boolean!
}
```

### **Client Usage**
```graphql
# First page
query GetPosts {
  posts(first: 10) {
    edges {
      cursor
      node { id title }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}

# Next page
query GetMorePosts($after: String!) {
  posts(first: 10, after: $after) {
    edges {
      cursor
      node { id title }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

---

## 🆔 **Global Object Identification**

### **Node Interface**
```graphql
interface Node {
  id: ID!
}

type User implements Node {
  id: ID!          # Global unique identifier
  displayName: String!
  email: String!
}

type Post implements Node {
  id: ID!          # Global unique identifier
  title: String!
  content: String!
  author: User!
}
```

### **Node Query**
```graphql
type Query {
  node(id: ID!): Node
  nodes(ids: [ID!]!): [Node]!
}

# Client can fetch any object by global ID
query GetAnyNode($id: ID!) {
  node(id: $id) {
    id
    ... on User {
      displayName
      email
    }
    ... on Post {
      title
      content
    }
  }
}
```

---

## 💾 **Caching Strategies**

### **Query-Level Caching**
```graphql
# Cache entire query results
query GetUserProfile($id: ID!) @cached(ttl: 300) {
  user(id: $id) {
    id
    displayName
    profileImageUrl
  }
}
```

### **Field-Level Caching**
```graphql
type User {
  id: ID!
  displayName: String! @cached(ttl: 3600)
  posts: [Post!]! @cached(ttl: 300)
}
```

### **Client-Side Caching**
- **Normalized cache**: Store objects by global ID
- **Cache invalidation**: Update cache when mutations occur
- **Optimistic updates**: Update UI immediately, rollback on errors
- **Cache-first**: Serve from cache when available

---

## ⚡ **Performance Optimization**

### **Query Complexity Analysis**
```javascript
// Limit query complexity to prevent abuse
const depthLimit = require('graphql-depth-limit');
const costAnalysis = require('graphql-cost-analysis');

const server = new GraphQLServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(10),
    costAnalysis.createComplexityLimitRule(1000)
  ]
});
```

### **DataLoader Pattern**
```javascript
// Batch and cache database requests
const DataLoader = require('dataloader');

const userLoader = new DataLoader(async (userIds) => {
  const users = await User.findByIds(userIds);
  return userIds.map(id => users.find(user => user.id === id));
});

// Resolver using DataLoader
const resolvers = {
  Post: {
    author: (post) => userLoader.load(post.authorId)
  }
};
```

### **Query Timeout**
```javascript
// Set timeout for long-running queries
const server = new GraphQLServer({
  typeDefs,
  resolvers,
  plugins: [
    {
      requestDidStart() {
        return {
          willSendResponse(requestContext) {
            if (requestContext.elapsed > 30000) {
              throw new Error('Query timeout');
            }
          }
        };
      }
    }
  ]
});
```

---

## 🔒 **Security Best Practices**

### **Query Depth Limiting**
```javascript
// Prevent deeply nested queries
const depthLimit = require('graphql-depth-limit');

const server = new GraphQLServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(10)]
});
```

### **Rate Limiting**
```javascript
// Implement query-based rate limiting
const costAnalysis = require('graphql-cost-analysis');

const server = new GraphQLServer({
  typeDefs,
  resolvers,
  validationRules: [
    costAnalysis.createComplexityLimitRule(1000, {
      createError: (max, actual) => {
        throw new Error(`Query too complex: ${actual}. Maximum allowed: ${max}`);
      }
    })
  ]
});
```

### **Input Validation**
```graphql
# Use scalar types for validation
scalar EmailAddress
scalar URL
scalar DateTime

type User {
  email: EmailAddress!
  website: URL
  createdAt: DateTime!
}

input CreateUserInput {
  displayName: String! @length(min: 2, max: 50)
  email: EmailAddress!
  password: String! @length(min: 8)
}
```

---

## 🧪 **Testing GraphQL APIs**

### **Schema Testing**
```javascript
// Test schema validity
const { buildSchema } = require('graphql');

test('schema is valid', () => {
  expect(() => buildSchema(typeDefs)).not.toThrow();
});
```

### **Query Testing**
```javascript
// Test queries against schema
const { graphql } = require('graphql');

test('user query returns expected data', async () => {
  const query = `
    query GetUser($id: ID!) {
      user(id: $id) {
        id
        displayName
      }
    }
  `;

  const result = await graphql(schema, query, null, context, { id: '123' });

  expect(result.errors).toBeUndefined();
  expect(result.data.user.id).toBe('123');
});
```

### **Resolver Testing**
```javascript
// Test individual resolvers
test('user resolver returns user data', async () => {
  const user = await resolvers.Query.user(null, { id: '123' }, context);

  expect(user.id).toBe('123');
  expect(user.displayName).toBeDefined();
});
```

---

## 📈 **Schema Evolution**

### **Additive Changes (Safe)**
```graphql
# ✅ Safe changes that don't break existing clients
type User {
  id: ID!
  displayName: String!
  email: String!
  # New optional field
  profileImageUrl: String
}

type Query {
  user(id: ID!): User
  # New query field
  users(limit: Int): [User!]!
}
```

### **Breaking Changes (Avoid)**
```graphql
# ❌ Breaking changes that can break existing clients
type User {
  id: ID!
  displayName: String!
  # Removed field - BREAKING
  # email: String!

  # Changed field type - BREAKING
  age: String!  # Was Int! before
}
```

### **Deprecation Strategy**
```graphql
type User {
  id: ID!
  displayName: String!
  email: String!

  # Deprecated field with reason
  username: String! @deprecated(reason: "Use displayName instead")
}
```

---

## 🚀 **Development Tools**

### **GraphQL Playground/Apollo Studio**
- **Interactive query exploration**: Test queries in browser
- **Schema documentation**: Auto-generated docs from schema
- **Query validation**: Real-time validation and autocompletion

### **Code Generation**
- **Client code generation**: Generate TypeScript types from schema
- **Server boilerplate**: Generate resolver stubs from schema
- **Documentation**: Generate API docs from schema

### **Schema Stitching/Federation**
- **Microservices**: Combine multiple GraphQL services
- **Gateway pattern**: Single GraphQL endpoint for multiple services
- **Schema composition**: Declarative schema merging

---

## 📚 **Schema Documentation**

### **Description Fields**
```graphql
"""
Represents a user in the system
"""
type User {
  """
  Unique identifier for the user
  """
  id: ID!

  """
  Display name shown to other users
  """
  displayName: String!

  """
  User's email address (private)
  """
  email: String!
}
```

### **Custom Directives**
```graphql
directive @auth(requires: Role = USER) on FIELD_DEFINITION

type User {
  id: ID!
  displayName: String!
  email: String! @auth(requires: ADMIN)
}
```

---

## ⚡ **Quick Reference Checklist**

### **✅ GraphQL API Checklist**
- [ ] Design schema around client needs, not database structure
- [ ] Use strong typing with appropriate nullable/non-nullable fields
- [ ] Implement proper pagination using connections
- [ ] Use global object identification with Node interface
- [ ] Implement field-level authorization
- [ ] Add query depth and complexity limits
- [ ] Use DataLoader pattern to prevent N+1 queries
- [ ] Implement proper error handling with structured errors
- [ ] Add query timeout protection
- [ ] Document schema with descriptions
- [ ] Write comprehensive tests for schema, queries, and resolvers
- [ ] Plan for schema evolution and deprecation
- [ ] Implement caching at appropriate levels
- [ ] Use introspection for development tools
- [ ] Monitor query performance and complexity

---

## 🔗 **Additional Resources**

- [GraphQL Official Documentation](https://graphql.org/learn/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Apollo Server Documentation](https://www.apollographql.com/docs/apollo-server/)
- [GraphQL Code Generator](https://www.graphql-code-generator.com/)
- [DataLoader Documentation](https://github.com/graphql/dataloader)
- [GraphQL Specification](https://spec.graphql.org/)

---

**Last Updated**: January 2025
**Version**: 1.0
**License**: MIT
**Based on**: [GraphQL Foundation Best Practices](https://graphql.org/learn/best-practices/)
