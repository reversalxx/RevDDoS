# RevDDoS

A lightweight ddos testing tool inspired by [MHDDoS](https://github.com/MatrixTM/MHDDoS).

## What This Tool Does

This script allows you to simulate two types of network attacks:

- Http Flood: Sends multiple http requests to a target website
- Tcp Flood: Establishes multiple tcp connections to a target server

## Requirements

- Python 3.7 or higher
- Required library: requests

Install the required library with:
`pip install requests`

## How To Use

Basic command structure:
`python3 script.py <target_url> [method] [duration] [threads] [use_proxies]`

### Parameters Explained

- `target_url`: The website you want to test (required)
- `method`: Type of attack - 'http' or 'tcp' (default: http)
- `duration`: How long the test runs in seconds (default: 60)
- `threads`: How many simultaneous connections to make (default: 10)
- `use_proxies`: Whether to use proxies - 'true' or 'false' (default: true)

### Example Commands

Test a website for 60 seconds with 10 threads using http method:
`python3 script.py http://example.com`

Test a website for 2 minutes with 20 threads using tcp method without proxies:
`python3 script.py http://example.com tcp 120 20 false`

Test a website with custom duration and thread count:
`python3 script.py http://example.com http 300 50 true`

## How It Works

1. The script automatically fetches proxies from multiple public sources when enabled
2. It creates multiple threads that simultaneously send requests to the target
3. Each request uses random user agents and referers for realistic traffic patterns
4. The script displays real-time statistics about the attack progress
5. When the duration expires, it shows a summary of total requests sent

## Important Notes

- This tool is for educational purposes only
- Always get proper authorization before testing any website
- Do not use this tool against websites you don't own or have permission to test
- The author is not responsible for any misuse of this tool
- Using proxies helps with anonymity but doesn't guarantee complete protection

## Troubleshooting

If you encounter issues:
1. Make sure Python 3.7+ is installed
2. Verify the requests library is installed: `pip install requests`
3. Ensure you have a stable internet connection for proxy fetching
