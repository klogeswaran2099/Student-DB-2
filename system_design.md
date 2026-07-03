# Task 2.1 — Requirements

**Functional Requirements:**
1. Students can view their examination marks.
2. Students can enroll in available courses.
3. Admins can manage student, course, and faculty records.

**Non-Functional Requirements:**
1. Support 50,000 concurrent users during peak loads (Scalability).
2. Data must survive a database server crash (Reliability).
3. Only authenticated users can access academic records (Security).

# Task 2.2 — High-Level Design

**a. Main Components**
* **Auth Service:** Issues and validates session tokens. Exposes a REST API.
* **Student Portal:** Handles student workflows (marks, enrollment). Exposes an HTML/JSON web interface to users and queries the DB.
* **Admin Panel:** Handles staff CRUD operations. Exposes a web interface to staff and queries the DB.

**b. Layered Architecture (Student Portal)**
* **Presentation Layer:** Renders the UI and handles HTTP requests. Receives user input (clicks, form data) and passes commands to the business layer.
* **Business Layer:** Enforces rules (e.g., checking course capacity). Receives commands from the presentation layer, runs logic, and requests data from the DAL.
* **Data Access Layer (DAL):** Executes database queries. Receives object requests from the business layer and passes back database rows mapped to objects.

**c. Scaling Strategy**
I would use **horizontal scaling** for the web servers to handle the 50,000 users. It is cheaper and more fault-tolerant to add multiple commodity servers than trying to build one massive server (vertical scaling). 
Traffic would be distributed using the **Least Connections** load-balancing algorithm. This is suitable because some user sessions (enrolling in classes) take much longer than others (checking a grade), so this prevents any single server from getting clogged with long-running requests.

**d. Elasticity**
Elasticity allows the infrastructure to automatically scale down to 1-2 servers during off-peak times (semester break) to save on cloud compute costs, and automatically provision new servers specifically for the few hours when exam results are published.

**e. Session Routing Problem**
* **Problem:** Loss of Session State (Server B doesn't share Server A's local memory).
* **Strategy 1 (Routing):** Sticky Sessions. The load balancer always sends a user to their initial server. *Trade-off:* Can lead to uneven load distribution.
* **Strategy 2 (Storage):** Centralized Session Store (e.g., Redis). All servers check a shared external cache. *Trade-off:* Adds network latency and infrastructure cost.
