# Bobtail
A little Python http framework


## Install
```
pip install bobtail
```

### Getting Started
```python

class Images:

    def get(self):
        return f"It Works!"

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


routes = [
    (Images, "/images")
]

app = BobTail(routes=routes)

```
