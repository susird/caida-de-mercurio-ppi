from core.app import App

def main():
    try:
        App().run()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()
