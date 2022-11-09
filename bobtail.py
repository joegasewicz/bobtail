from wsgi import BobTail


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

if __name__ == "__main__":
    print(f"Bobtail!")

