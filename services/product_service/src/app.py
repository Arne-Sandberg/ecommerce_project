from src.clients.post import PostRestClient


def main():
    client = PostRestClient()
    for _id in range(1, 10):
        model = client.get_one(_id)
        print(model)


if __name__ == '__main__':
    main()
