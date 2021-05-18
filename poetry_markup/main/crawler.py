import subprocess
import sys

if __name__ == "__main__":

    proc = subprocess.Popen(["scrapy", "crawl", "poems"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True)
    for line in proc.stdout:
        sys.stdout.write(line)
    proc.wait()

    proc = subprocess.Popen(["scrapy", "crawl", "poems1"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True)
    for line in proc.stdout:
        sys.stdout.write(line)
    proc.wait()

    proc = subprocess.Popen(["scrapy", "crawl", "dictionary"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True)
    for line in proc.stdout:
        sys.stdout.write(line)
    proc.wait()
