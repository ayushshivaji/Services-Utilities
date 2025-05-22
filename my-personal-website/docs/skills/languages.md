# Programming Languages

## Languages I Use Regularly

### JavaScript/TypeScript
JavaScript and TypeScript are my primary languages for web and cross-platform development.

**Experience Level:** Expert (5+ years)  
**Projects Completed:** 30+  
**Key Libraries/Frameworks:** React, Vue.js, Node.js, Express, Next.js  

**Code Sample:**
```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

const getUsers = async (): Promise<User[]> => {
  try {
    const response = await fetch('/api/users');
    const data = await response.json();
    return data.users;
  } catch (error) {
    console.error('Error fetching users:', error);
    return [];
  }
};
```

### Python
Python is my go-to language for data science, automation, and backend development.

**Experience Level:** Advanced (4+ years)  
**Projects Completed:** 20+  
**Key Libraries/Frameworks:** Django, Flask, Pandas, NumPy, TensorFlow  

**Code Sample:**
```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def train_model(data_path, target_column):
    # Load and prepare data
    df = pd.read_csv(data_path)
    X = df.drop(target_column, axis=1)
    y = df[target_column]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    return model
```

### Go
I use Go for building high-performance microservices and concurrent applications.

**Experience Level:** Intermediate (2+ years)  
**Projects Completed:** 5+  
**Key Libraries/Frameworks:** Gin, GORM, Echo  

**Code Sample:**
```go
package main

import (
	"encoding/json"
	"log"
	"net/http"
	"github.com/gorilla/mux"
)

type Task struct {
	ID        string `json:"id"`
	Title     string `json:"title"`
	Completed bool   `json:"completed"`
}

var tasks []Task

func getTasks(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(tasks)
}

func main() {
	router := mux.NewRouter()
	
	// Initialize with some data
	tasks = append(tasks, Task{ID: "1", Title: "Complete project", Completed: false})
	
	// Routes
	router.HandleFunc("/api/tasks", getTasks).Methods("GET")
	
	// Start server
	log.Fatal(http.ListenAndServe(":8000", router))
}
```

## Other Languages

### Java
Used for enterprise applications and Android development.

**Experience Level:** Intermediate  
**Key Projects:** Enterprise CRM, Android applications  

### C/C++
Used for systems programming and performance-critical applications.

**Experience Level:** Basic to Intermediate  
**Key Projects:** Embedded systems, algorithm implementations  

### Swift
Used for iOS application development.

**Experience Level:** Basic to Intermediate  
**Key Projects:** Weather app, fitness tracker  

## Learning Next

I'm currently expanding my knowledge in:

- **Rust**: For systems programming with memory safety
- **Kotlin**: For more advanced Android development
- **Solidity**: For blockchain and smart contract development 