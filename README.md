# Presistant B+tree

![Database color animation meme](colorful-database-animation.gif)

Why did I refuse to use a databes?

Because it's wayyyy easier to create my own from scratch, here see

```python3
class MyAmazingDatabase:
    def __init__(self):
        self.data = {}

    def insert(self, key, value):
        self.data[key] = value

    def fetch(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key in self.data:
            del self.data[key]
```

Developing a fully functional embedded database from the ground up. The goal is to implement various features and optimizations present in popular databases such as SQLite3, MongoDB, UQLite, and others.

The primary objective is to gain a better understanding of how these databases work under the hood and learn about the intricacies involved in their design and implementation. This hands-on approach will provide valuable insights into the inner workings of embedded databases, allowing for a more comprehensive understanding of their structure, performance, and capabilities. By creating a custom embedded database, the project aims to serve as a learning experience that will enhance the developer's knowledge and skills in database design and optimization.
