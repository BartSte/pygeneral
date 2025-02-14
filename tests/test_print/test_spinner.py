from time import sleep

from pygeneral.print.rotator import Rotator

if __name__ == "__main__":
    animation = Rotator(
        chars=["T", "Te", "Tes", "Test", "Testi", "Testin", "Testing"],
        prefix="Working: ",
        suffix="...",
    )
    for _ in range(100):
        animation.value += 1
        sleep(0.1)
        print(animation.make_message(), end="")
