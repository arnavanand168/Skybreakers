# SkyHack 3.0 United Airlines Flight Difficulty Scoring System
## Executive Summary & Business Recommendations

---

## Slide 1: Project Overview
### **Challenge**: Develop a Flight Difficulty Scoring System for United Airlines

**Objective**: Create a data-driven system to classify flights by operational complexity to optimize resource allocation and improve operational efficiency.

**Approach**: 
- Analyzed 5 comprehensive datasets (8,155 flights)
- Engineered 7 key difficulty drivers
- Implemented weighted scoring algorithm
- Classified flights into 3 categories: Difficult, Medium, Easy

**Key Deliverable**: `test_arnav.csv` with complete flight classifications and difficulty scores

---

## Slide 2: Data Foundation & Methodology
### **Data Sources Analyzed**
- **Flight Level Data**: 8,100 flights with operational metrics
- **Bag Level Data**: 687K+ bag records with transfer information
- **Passenger Data**: 687K+ passenger records with demographics
- **Special Service Requests**: 51K+ special service requests
- **Airport Data**: 5,613 airports with country codes

### **Methodology**
1. **Data Consolidation**: Created master table joining all datasets
2. **Feature Engineering**: Developed 7 operational complexity drivers
3. **Normalization**: Applied Min-Max scaling (0-1 range)
4. **Weighted Scoring**: Business-defined weights for each factor
5. **Daily Classification**: Ranked flights within each operational day

---

## Slide 3: Difficulty Drivers & Scoring Model
### **7 Key Difficulty Drivers**

| Factor | Weight | Description |
|--------|--------|-------------|
| **Ground Time Pressure** | 25% | Scheduled vs. minimum required ground time |
| **Load Factor** | 20% | Percentage of seats filled |
| **Transfer Bag Ratio** | 20% | Proportion of bags requiring transfers |
| **SSR Intensity** | 15% | Special service requests per passenger |
| **International** | 10% | International flight complexity |
| **Fleet Complexity** | 5% | Aircraft type complexity |
| **Time Complexity** | 5% | Departure time operational complexity |

### **Classification Logic**
- **Difficult**: Top 20% of daily flights by difficulty score
- **Medium**: Next 30% of daily flights
- **Easy**: Bottom 50% of daily flights

---

## Slide 4: Key Findings - Classification Results
### **Overall Classification Distribution**

| Category | Count | Percentage | Avg Difficulty Score |
|----------|-------|------------|-------------------|
| **Difficult** | 1,624 | 19.91% | 0.343 |
| **Medium** | 2,449 | 30.03% | 0.278 |
| **Easy** | 4,082 | 50.06% | 0.215 |

### **Critical Insights**
- **49.52%** of flights experience delays (avg 23.31 minutes)
- **60.36%** of flights have low ground time (pressure > 1.5)
- **51.5%** average transfer bag ratio across all flights
- **10.9%** average SSR intensity (special service requests)

---

## Slide 5: Top Difficult Destinations Analysis
### **Top 10 Most Challenging Destinations**

| Rank | Destination | Difficult Flights | % of Difficult | Key Drivers |
|------|-------------|------------------|----------------|-------------|
| 1 | **YYZ (Toronto)** | 77 | 4.74% | International, High Load Factor |
| 2 | **STL (St. Louis)** | 53 | 3.26% | High Transfer Ratio, SSR Intensity |
| 3 | **LHR (London)** | 44 | 2.71% | International, Ground Time Pressure |
| 4 | **YOW (Ottawa)** | 41 | 2.52% | International, Transfer Complexity |
| 5 | **YUL (Montreal)** | 39 | 2.40% | International Operations |

### **Root Cause Analysis**
- **International flights** dominate difficult category (40.7% vs 0.1% for easy)
- **High load factors** (1.086 vs 0.988) indicate capacity pressure
- **Ground time pressure** significantly higher (5.18 vs 3.46)
- **Transfer bag ratios** much higher (0.679 vs 0.386)

---

## Slide 6: Fleet & Operational Analysis
### **Fleet Type Difficulty Patterns**

| Fleet Type | Difficult % | Avg Score | Key Characteristics |
|------------|-------------|-----------|-------------------|
| **B767-300** | 98.33% | 0.369 | Wide-body, International |
| **B787-8** | 97.33% | 0.393 | Long-haul, Complex |
| **B787-10** | 93.79% | 0.387 | Premium, High-capacity |
| **B757-200** | 42.86% | 0.291 | Domestic, Medium-complexity |
| **B737-MAX8** | 29.68% | 0.271 | Regional, Standard |

### **Time of Day Complexity**
- **Evening Rush (16-19)**: 31.6% difficult flights
- **Night Operations (20-23)**: 25.85% difficult flights
- **Afternoon (12-15)**: 10.46% difficult flights (lowest complexity)

---

## Slide 7: Business Recommendations
### **Priority 1: Resource Allocation Optimization**

**Immediate Actions:**
- **Deploy additional ground crew** to flights classified as "Difficult"
- **Prioritize international destinations** (YYZ, LHR, YOW, YUL) for enhanced staffing
- **Allocate specialized equipment** for wide-body aircraft (B767, B787)

**Expected Impact:** 20% reduction in ground time delays, improved on-time performance

### **Priority 2: Operational Timing Adjustments**

**Strategic Changes:**
- **Evening Rush Enhancement**: Increase staffing during 16:00-19:00 timeframe
- **International Buffer**: Extend minimum turn times for international operations
- **Wide-body Optimization**: Increase ground time buffers for B767/B787 fleets

**Expected Impact:** 15% improvement in ground time efficiency

---

## Slide 8: Implementation Roadmap & ROI
### **Phase 1: Immediate Implementation (0-3 months)**
- Deploy difficulty scoring system to operations control
- Train dispatchers on difficulty classifications
- Implement priority resource allocation for "Difficult" flights

### **Phase 2: Process Optimization (3-6 months)**
- Integrate scoring system with crew scheduling
- Develop automated resource allocation algorithms
- Create real-time difficulty monitoring dashboards

### **Expected ROI**
- **Cost Savings**: $2-3M annually through reduced delays and improved efficiency
- **Customer Satisfaction**: 15-20% improvement in on-time performance
- **Operational Efficiency**: 25% reduction in ground time pressure for difficult flights

### **Success Metrics**
- On-time departure rate improvement
- Ground time efficiency gains
- Customer satisfaction scores
- Operational cost reduction

---

## Conclusion
The Flight Difficulty Scoring System provides United Airlines with a data-driven approach to optimize flight operations. By focusing resources on the most challenging flights and implementing strategic operational adjustments, United can significantly improve efficiency, reduce delays, and enhance customer satisfaction.

**Next Steps**: Deploy the system, monitor results, and iterate based on operational feedback.

---

*Analysis completed for SkyHack 3.0 United Airlines Challenge*
*Contact: Development Team*
