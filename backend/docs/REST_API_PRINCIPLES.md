# REST API Design Principles

**Comprehensive guide for designing and implementing RESTful APIs following industry best practices.**

> 📖 **Usage**: This document serves as a generic guide for REST API development that can be applied to any project requiring RESTful API design.

---

## 🎯 **Core REST Principles**

### **1. Uniform Interface**
- **Resource-based URLs**: Use nouns, not verbs in endpoints
- **HTTP methods**: Use appropriate HTTP verbs for different operations
- **Stateless communication**: Each request contains all necessary information
- **Self-descriptive messages**: Include proper content types and metadata

### **2. Client-Server Architecture**
- **Separation of concerns**: UI concerns separated from data storage concerns
- **Independent evolution**: Client and server can evolve independently
- **Platform independence**: Any client can communicate with any server

### **3. Statelessness**
- **No server-side sessions**: All session state stored on client
- **Complete requests**: Each request from client contains all information needed
- **Scalability**: Enables horizontal scaling and load balancing

### **4. Cacheability**
- **Cache-Control headers**: Explicit caching instructions
- **ETags**: Entity tags for cache validation
- **Conditional requests**: If-None-Match, If-Modified-Since headers

### **5. Layered System**
- **Intermediate servers**: Proxies, gateways, load balancers allowed
- **Transparency**: Clients unaware of intermediate layers
- **Security**: Additional security layers can be added

### **6. Code on Demand (Optional)**
- **Dynamic behavior**: Server can send executable code to client
- **JavaScript**: Most common example in web applications
- **Plugins**: Downloadable components to extend client functionality

---

## 🛠️ **HTTP Methods & Usage**

### **GET** - Retrieve Resources
```http
GET /api/v1/users           # List all users
GET /api/v1/users/123       # Get specific user
GET /api/v1/users/123/posts # Get user's posts
```
- **Idempotent**: Multiple identical requests have same effect
- **Safe**: No side effects on server state
- **Cacheable**: Responses can be cached

### **POST** - Create Resources
```http
POST /api/v1/users          # Create new user
POST /api/v1/users/123/posts # Create post for user
```
- **Non-idempotent**: Multiple requests may have different effects
- **Not safe**: Modifies server state
- **Not cacheable**: Responses typically not cached

### **PUT** - Update/Replace Resources
```http
PUT /api/v1/users/123       # Replace entire user resource
```
- **Idempotent**: Multiple identical requests have same effect
- **Not safe**: Modifies server state
- **Complete replacement**: Entire resource is replaced

### **PATCH** - Partial Updates
```http
PATCH /api/v1/users/123     # Partially update user
```
- **Non-idempotent**: May have different effects
- **Not safe**: Modifies server state
- **Partial update**: Only specified fields are updated

### **DELETE** - Remove Resources
```http
DELETE /api/v1/users/123    # Delete specific user
```
- **Idempotent**: Multiple requests have same effect
- **Not safe**: Modifies server state
- **Resource removal**: Removes the specified resource

---

## 📍 **URL Design Principles**

### **Resource Naming Conventions**
```http
# ✅ GOOD - Use nouns for resources
GET /api/v1/users
GET /api/v1/products
GET /api/v1/orders

# ❌ BAD - Avoid verbs in URLs
GET /api/v1/getUsers
GET /api/v1/createProduct
POST /api/v1/deleteOrder
```

### **Hierarchical Relationships**
```http
# Parent-child relationships
GET /api/v1/users/123/orders        # Orders for specific user
GET /api/v1/orders/456/items        # Items in specific order
GET /api/v1/categories/789/products # Products in category
```

### **Collection vs. Individual Resources**
```http
# Collections (plural nouns)
GET /api/v1/users              # All users
POST /api/v1/users             # Create user

# Individual resources
GET /api/v1/users/123          # Specific user
PUT /api/v1/users/123          # Update specific user
DELETE /api/v1/users/123       # Delete specific user
```

### **Query Parameters for Filtering**
```http
# Filtering
GET /api/v1/users?status=active&role=admin

# Pagination
GET /api/v1/users?page=2&limit=20

# Sorting
GET /api/v1/users?sort=created_at&order=desc

# Searching
GET /api/v1/users?search=john&fields=name,email
```

---

## 📊 **HTTP Status Codes**

### **2xx Success**
- **200 OK**: Request succeeded (GET, PUT, PATCH)
- **201 Created**: Resource created successfully (POST)
- **202 Accepted**: Request accepted for processing (async operations)
- **204 No Content**: Success with no response body (DELETE)

### **3xx Redirection**
- **301 Moved Permanently**: Resource permanently moved
- **302 Found**: Resource temporarily moved
- **304 Not Modified**: Resource not modified (caching)

### **4xx Client Errors**
- **400 Bad Request**: Invalid request syntax or parameters
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Authentication provided but insufficient permissions
- **404 Not Found**: Resource not found
- **405 Method Not Allowed**: HTTP method not supported for resource
- **409 Conflict**: Request conflicts with current resource state
- **422 Unprocessable Entity**: Validation errors
- **429 Too Many Requests**: Rate limiting

### **5xx Server Errors**
- **500 Internal Server Error**: Generic server error
- **501 Not Implemented**: Server doesn't support requested functionality
- **502 Bad Gateway**: Invalid response from upstream server
- **503 Service Unavailable**: Server temporarily unavailable
- **504 Gateway Timeout**: Timeout from upstream server

---

## 🔒 **Security Best Practices**

### **Authentication & Authorization**
```http
# Bearer token authentication
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# API key authentication
X-API-Key: your-api-key-here

# Basic authentication (HTTPS only)
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

### **HTTPS Only**
- **Encrypt all communication**: Never use HTTP for APIs
- **TLS 1.2+ required**: Use modern TLS versions
- **Certificate validation**: Proper SSL certificate setup

### **Input Validation**
- **Sanitize inputs**: Validate all incoming data
- **Parameter validation**: Check data types, ranges, formats
- **SQL injection prevention**: Use parameterized queries
- **XSS prevention**: Escape output appropriately

### **Rate Limiting**
```http
# Rate limit headers
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

---

## 📝 **Request/Response Format**

### **JSON as Default**
```http
Content-Type: application/json
Accept: application/json
```

### **Request Body Structure**
```json
{
  "data": {
    "type": "users",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

### **Response Body Structure**
```json
{
  "data": {
    "id": "123",
    "type": "users",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2023-01-15T10:30:00Z"
    }
  },
  "meta": {
    "timestamp": "2023-01-15T10:30:00Z",
    "version": "1.0"
  }
}
```

### **Error Response Structure**
```json
{
  "errors": [
    {
      "id": "validation_error",
      "status": "422",
      "code": "INVALID_EMAIL",
      "title": "Invalid email format",
      "detail": "The email field must be a valid email address",
      "source": {
        "pointer": "/data/attributes/email"
      }
    }
  ]
}
```

---

## 📄 **Pagination Strategies**

### **Offset-based Pagination**
```http
GET /api/v1/users?page=2&limit=20

# Response
{
  "data": [...],
  "meta": {
    "pagination": {
      "page": 2,
      "limit": 20,
      "total": 1000,
      "pages": 50
    }
  }
}
```

### **Cursor-based Pagination**
```http
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ&limit=20

# Response
{
  "data": [...],
  "meta": {
    "pagination": {
      "next_cursor": "eyJpZCI6MTQzfQ",
      "prev_cursor": "eyJpZCI6MTAzfQ",
      "has_more": true
    }
  }
}
```

---

## 🚀 **Performance Optimization**

### **Caching Headers**
```http
# Response headers
Cache-Control: public, max-age=3600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT

# Conditional requests
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT
```

### **Compression**
```http
# Request
Accept-Encoding: gzip, deflate, br

# Response
Content-Encoding: gzip
```

### **Field Selection**
```http
# Include only specific fields
GET /api/v1/users?fields=id,name,email

# Exclude specific fields
GET /api/v1/users?exclude=password,internal_notes
```

---

## 📚 **Versioning Strategies**

### **URL Path Versioning (Recommended)**
```http
GET /api/v1/users
GET /api/v2/users
```

### **Header Versioning**
```http
GET /api/users
Accept: application/vnd.myapi.v1+json
```

### **Query Parameter Versioning**
```http
GET /api/users?version=1
```

---

## 🧪 **Testing REST APIs**

### **Unit Tests**
- **Endpoint testing**: Test individual API endpoints
- **Business logic**: Test core functionality
- **Edge cases**: Test boundary conditions

### **Integration Tests**
- **Database integration**: Test data persistence
- **External services**: Test third-party integrations
- **Authentication flows**: Test security mechanisms

### **Contract Testing**
- **API contracts**: Ensure API meets consumer expectations
- **Schema validation**: Validate request/response schemas
- **Backward compatibility**: Ensure changes don't break existing clients

---

## 📖 **Documentation Best Practices**

### **OpenAPI/Swagger Specification**
```yaml
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Users retrieved successfully
```

### **Interactive Documentation**
- **Swagger UI**: Interactive API documentation
- **Postman collections**: Shareable API collections
- **Code examples**: Client implementation examples

---

## ⚡ **Quick Reference Checklist**

### **✅ REST API Checklist**
- [ ] Use appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE)
- [ ] Use nouns for resource URLs, not verbs
- [ ] Return appropriate HTTP status codes
- [ ] Implement proper error handling with structured error responses
- [ ] Use JSON as default content type
- [ ] Implement pagination for list endpoints
- [ ] Add authentication and authorization
- [ ] Use HTTPS for all communication
- [ ] Implement rate limiting
- [ ] Add proper caching headers
- [ ] Version your API appropriately
- [ ] Document with OpenAPI/Swagger
- [ ] Write comprehensive tests
- [ ] Validate all inputs
- [ ] Handle errors gracefully

---

## 🔗 **Additional Resources**

- [Roy Fielding's REST Dissertation](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
- [HTTP/1.1 Specification](https://tools.ietf.org/html/rfc7231)
- [OpenAPI Specification](https://swagger.io/specification/)
- [JSON API Specification](https://jsonapi.org/)
- [REST API Design Rulebook](https://www.oreilly.com/library/view/rest-api-design/9781449317904/)

---

**Last Updated**: January 2025
**Version**: 1.0
**License**: MIT
