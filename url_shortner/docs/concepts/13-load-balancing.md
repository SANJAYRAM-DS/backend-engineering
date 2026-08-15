# Concept 13 — Load Balancing Algorithms & Layer 4 vs Layer 7

# 1. Load Balancing Overview
A Load Balancer sits between clients and API servers, health-checking nodes and balancing HTTP traffic.

```text
                            [ Clients ]
                                 │
                                 ▼
                         [ Load Balancer ]
                         /       |       \
                        ▼        ▼        ▼
                      API 1    API 2    API 3
```

---

# 2. L4 vs L7 Load Balancing

- **Layer 4 (Transport Level)**: Routes TCP/UDP packets based on IP and Port without inspecting HTTP content. Ultra-fast (~1M QPS).
- **Layer 7 (Application Level)**: Inspects HTTP headers, paths (`/api/v1/*`), cookies, and SSL certificate termination.

### Balancing Algorithms
- **Round Robin**: Routes requests sequentially (Node 1 -> Node 2 -> Node 3).
- **Least Connections**: Directs traffic to node with fewest active connections.
- **IP Hash**: Ensures requests from same client IP land on same server node.
