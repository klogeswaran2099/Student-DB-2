# SARS Architecture & Design Rationales

## Task 2.1: Architecture Choice
I recommend a **Microservices architecture**. 
* **Independent Deployment:** We can push updates to the Admin Panel without restarting the Student Portal.
* **Fault Isolation:** If the Auth service crashes, it doesn't take down the entire system memory like a Monolith crash would.
* **Management Complexity:** It is harder to manage than a monolith, but necessary to hit the 50k user requirement efficiently.

## Task 2.3: SOLID & Design Patterns
* **Single Responsibility Principle:** `Student` manages student data only; email logic is excluded.
* **Open/Closed Principle:** `Enrollment` allows extending behaviors (via `WaitlistedEnrollment`) without modifying the base class.
* **Dependency Inversion Principle:** `Enrollment` depends on the `EnrollmentRepository` interface, not a concrete database implementation.
* **Observer Pattern (2.3d):** Decouples the Admin Panel from downstream actions. The panel just publishes an event, allowing us to add or remove notification services later without rewriting the Admin Panel code.

## Task 2.4: Redundancy & Fault Tolerance

**a. Database Redundancy**
Data is replicated across multiple servers. If the primary crashes, the replica is promoted. During the failover, write requests fail or queue, but read requests can continue.

**b. Microservices Fault Isolation**
This relies on **Fault Isolation**. In a monolith, an email crash takes down the shared process. In microservices, they run independently. The Student Portal code must use a **Try/Catch with a timeout** when calling the Email Service, silently catching the network failure and proceeding so the UI doesn't hang.

**c. Synchronous Replication**
* **Trade-off:** High write latency, as the primary waits for the replica's network acknowledgment before confirming the commit.
* **Failover State:** 1. The replica holds all acknowledged writes up to the crash (zero lag).
  2. A student reading from the new replica sees a strictly consistent database.
  3. The DBA must check the crashed primary's Write-Ahead Log (WAL) for any unacknowledged inflight transactions. If inaccessible, they must accept the gap and promote the replica.
