FIFO_PATH = "/tmp/stop_recording_signal"

def main():
    with open(FIFO_PATH, 'w') as fifo:
        fifo.write('stop')

if __name__ == "__main__":
    main()
