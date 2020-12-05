import quarantine.controller as c

def main():
    print("Hello world.")

    qc = c.QController()
    qc.initialise()
    qc.run()


if __name__ == "__main__":
    main()