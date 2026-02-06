import html
import random
import statistics
import string
import sys
import time

from wheezy.html.utils import escape_html_native as escape_html_replace

try:
    from wheezy.html.utils import escape_html
except ImportError:
    print("WARNING: using html.escape as placeholder for escape_html")
    escape_html = html.escape


def make_unicode(size, escape_ratio=0.01, unicode_ratio=0.2):
    ascii_safe = string.ascii_letters + string.digits + "     "
    escape_chars = '<>&"'

    unicode_chars = (
        "áéíóúñçüΩЖЖЯΔλあいうえお𠀋𠂢𠃌"  # mix of 2-byte and 4-byte
    )

    result = []
    for _ in range(size):
        r = random.random()
        if r < escape_ratio:
            result.append(random.choice(escape_chars))
        elif r < escape_ratio + unicode_ratio:
            result.append(random.choice(unicode_chars))
        else:
            result.append(random.choice(ascii_safe))
    return "".join(result)


def bench(func, data, loops):
    for _ in range(3):
        func(data)

    times = []
    for _ in range(loops):
        start = time.perf_counter()
        func(data)
        end = time.perf_counter()
        times.append(end - start)

    return times


def report(name, times, size):
    mean = statistics.mean(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0.0
    mb_per_sec = (
        (len(size.encode("utf-8")) / (1024 * 1024)) / mean
        if hasattr(size, "encode")
        else size / mean
    )
    print(
        f"{name:20} | "
        f"mean: {mean * 1000:8.3f} ms | "
        f"stdev: {stdev * 1000:6.3f} ms | "
        f"{mb_per_sec:8.2f} MB/s"
    )


def run_suite(size, escape_ratio, unicode_ratio, loops):
    print(
        f"\nSize: {size:,} chars, "
        f"escape_ratio={escape_ratio}, unicode_ratio={unicode_ratio}"
    )
    data = make_unicode(size, escape_ratio, unicode_ratio)

    if size < 100_000:
        assert escape_html(data) == html.escape(data)

    opt_times = bench(escape_html, data, loops)
    replace_times = bench(escape_html_replace, data, loops)
    std_times = bench(html.escape, data, loops)

    report("html_escape", opt_times, data)
    report("html_escape_replace", replace_times, data)
    report("html.escape", std_times, data)


def main():
    random.seed(0)

    sizes = [
        10,
        100,
        1_000,
        100_000,
        1_000_000,
    ]

    escape_ratios = [0.0, 0.01, 0.2]
    unicode_ratios = [0.0, 0.1, 0.2]

    loops = 200

    print(f"Python: {sys.version}")
    print("-" * 80)

    for size in sizes:
        for e_ratio in escape_ratios:
            for u_ratio in unicode_ratios:
                run_suite(size, e_ratio, u_ratio, loops)


if __name__ == "__main__":
    main()
