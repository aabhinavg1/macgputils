import macgputils

def main():
    stats = macgputils.get_gpu_stats()
    print("GPU Stats:", stats)

if __name__ == "__main__":
    main()
