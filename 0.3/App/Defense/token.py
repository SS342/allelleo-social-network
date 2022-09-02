import random


def generate_token(length=135):
    return str(
        ''.join(
            random.choice(
                list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-------')
            ) for i in range(
                length
            )
        )
    )

# print(generate_token())
