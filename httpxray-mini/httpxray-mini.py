#!/usr/bin/env python3
"""
HTTPxray-Mini - Single File Demo Version
Shows the power of HTTPxray in just 250 lines!

Run: python httpxray-mini.py -u https://example.com
"""

import requests
import json
import sys
import time
import threading
import os
from datetime import datetime
from urllib.parse import urlparse
from colorama import init, Fore, Style

# Initialize colors
init(autoreset=True)

# ==================== CONFIGURATION ====================
VERSION = "2.0.0-mini"
BANNER = f"""
{Fore.CYAN}

╔════════════════════════════════════════╗
║       HTTPxray-Mini v{VERSION}         ║
║                                        ║
║     Experience the FULL HTTPxray!      ║
║     Upgrade for ALL features:          ║
║     • Tech Detection • Security        ║
║     • Sensitive Data • ML • API        ║
║     • Reports • DB • Distributed       ║
║                                        ║
║ https://github.com/ssecgroup/httpxray  ║
╚════════════════════════════════════════╝{Style.RESET_ALL}
"""

# ==================== CORE SCANNER ====================
class HTTPxrayMini:
    """Single-file demo of HTTPxray capabilities"""
    
    def __init__(self, output_dir="outputs", verbose=False, threads=5):
        self.output_dir = output_dir
        self.verbose = verbose
        self.threads = threads
        self.results = []
        self.stats = {
            'total': 0,
            'status_codes': {},
            'redirects': 0,
            'errors': 0,
            'start_time': time.time()
        }
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"{Fore.GREEN}[✓] HTTPxray-Mini initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Output: {output_dir}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Threads: {threads}{Style.RESET_ALL}")
        print()
    
    def scan_url(self, url, method='GET'):
        """Scan a single URL"""
        try:
            start = time.time()
            
            # Make request
            response = requests.get(
                url,
                allow_redirects=True,
                timeout=10,
                headers={'User-Agent': 'HTTPxray-Mini/2.0'}
            )
            
            # Build result
            result = {
                'url': url,
                'method': method,
                'status': response.status_code,
                'time': round(time.time() - start, 3),
                'size': len(response.content),
                'content_type': response.headers.get('Content-Type', ''),
                'timestamp': datetime.now().isoformat()
            }
            
            # Track redirects
            if response.history:
                result['redirect_count'] = len(response.history)
                result['redirect_chain'] = [
                    {'url': r.url, 'status': r.status_code}
                    for r in response.history
                ]
                self.stats['redirects'] += len(response.history)
            
            # Quick tech detection (simplified)
            techs = []
            server = response.headers.get('Server', '')
            if server:
                techs.append({'technology': server.split('/')[0], 'confidence': 'high'})
            
            if 'X-Powered-By' in response.headers:
                techs.append({'technology': response.headers['X-Powered-By'], 'confidence': 'medium'})
            
            if techs:
                result['technologies'] = techs
            
            # Quick security check (simplified)
            security_issues = []
            security_score = 100
            
            # Check common security headers
            if 'Strict-Transport-Security' not in response.headers:
                security_issues.append('missing_hsts')
                security_score -= 10
            if 'Content-Security-Policy' not in response.headers:
                security_issues.append('missing_csp')
                security_score -= 10
            if 'X-Frame-Options' not in response.headers:
                security_issues.append('missing_xfo')
                security_score -= 8
            if 'X-Content-Type-Options' not in response.headers:
                security_issues.append('missing_xcto')
                security_score -= 7
            
            if security_issues:
                result['security'] = {
                    'score': security_score,
                    'issues': security_issues,
                    'rating': self._get_rating(security_score)
                }
            
            # Quick sensitive data check (simplified)
            sensitive = []
            text = response.text.lower()
            
            # Check for common patterns
            if 'api_key' in text or 'apikey' in text:
                sensitive.append({'type': 'api_key', 'severity': 'critical'})
            if '@' in text and '.' in text and 'mailto:' in text:
                sensitive.append({'type': 'email', 'severity': 'medium'})
            if 'password' in text or 'passwd' in text:
                sensitive.append({'type': 'password', 'severity': 'critical'})
            if 'secret' in text:
                sensitive.append({'type': 'secret', 'severity': 'high'})
            
            if sensitive:
                result['sensitive_data'] = {
                    'count': len(sensitive),
                    'findings': sensitive
                }
            
            # Update stats
            self.stats['total'] += 1
            status_str = str(response.status_code)
            self.stats['status_codes'][status_str] = self.stats['status_codes'].get(status_str, 0) + 1
            
            # Save result
            self.results.append(result)
            self._save_result(result)
            
            # Print live output
            self._print_result(result)
            
            return result
            
        except Exception as e:
            error_result = {
                'url': url,
                'error': str(e),
                'status': 0,
                'timestamp': datetime.now().isoformat()
            }
            self.results.append(error_result)
            self.stats['errors'] += 1
            
            if self.verbose:
                print(f"{Fore.RED}[ERROR] {url} - {e}{Style.RESET_ALL}")
            
            return error_result
    
    def _get_rating(self, score):
        """Get security rating"""
        if score >= 80: return "A - Excellent"
        if score >= 60: return "B - Good"
        if score >= 40: return "C - Fair"
        if score >= 20: return "D - Poor"
        return "F - Critical"
    
    def _print_result(self, result):
        """Print colored result"""
        status = result.get('status', 0)
        
        if 200 <= status < 300:
            color = Fore.GREEN
        elif 300 <= status < 400:
            color = Fore.YELLOW
        elif 400 <= status < 500:
            color = Fore.MAGENTA
        elif 500 <= status < 600:
            color = Fore.RED
        else:
            color = Fore.WHITE
        
        # Build info badges
        badges = []
        
        if result.get('technologies'):
            badges.append(f"{Fore.MAGENTA}[T{len(result['technologies'])}]{Style.RESET_ALL}")
        
        if result.get('security'):
            score = result['security']['score']
            if score < 40:
                badge_color = Fore.RED
            elif score < 70:
                badge_color = Fore.YELLOW
            else:
                badge_color = Fore.GREEN
            badges.append(f"{badge_color}[S{score}]{Style.RESET_ALL}")
        
        if result.get('sensitive_data'):
            count = result['sensitive_data']['count']
            badges.append(f"{Fore.RED}[!{count}]{Style.RESET_ALL}")
        
        redirect = f" [{result.get('redirect_count', 0)}r]" if result.get('redirect_count') else ""
        
        # Print with progress
        progress = f"[{self.stats['total']}] "
        print(f"{color}{progress}[{status}]{Style.RESET_ALL} {result['url']}{redirect} {' '.join(badges)} ({result.get('time', 0)}s)")
        
        # Show details in verbose mode
        if self.verbose and result.get('security'):
            print(f"  {Fore.YELLOW}Security:{Style.RESET_ALL} Score {result['security']['score']} - {result['security']['rating']}")
        
        if self.verbose and result.get('sensitive_data'):
            print(f"  {Fore.RED}Sensitive:{Style.RESET_ALL} Found {result['sensitive_data']['count']} items")
    
    def _save_result(self, result):
        """Save result to file"""
        filename = f"{self.output_dir}/results.jsonl"
        with open(filename, 'a') as f:
            f.write(json.dumps(result) + '\n')
    
    def scan_file(self, filename):
        """Scan URLs from file"""
        print(f"{Fore.CYAN}[*] Scanning URLs from: {filename}{Style.RESET_ALL}")
        
        with open(filename, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        print(f"{Fore.CYAN}[*] Total URLs: {len(urls)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Starting {self.threads} threads...{Style.RESET_ALL}\n")
        
        # Simple threading
        threads = []
        for url in urls:
            while len(threads) >= self.threads:
                threads = [t for t in threads if t.is_alive()]
                time.sleep(0.1)
            
            t = threading.Thread(target=self.scan_url, args=(url,))
            t.start()
            threads.append(t)
        
        # Wait for completion
        for t in threads:
            t.join()
        
        self._show_summary()
    
    def scan_domain(self, domain):
        """Scan common paths on domain"""
        if not domain.startswith(('http://', 'https://')):
            domain = 'https://' + domain
        
        paths = [
            '/', '/robots.txt', '/sitemap.xml', '/admin', '/api',
            '/login', '/.env', '/.git/config', '/backup', '/test'
        ]
        
        print(f"{Fore.CYAN}[*] Scanning domain: {domain} ({len(paths)} paths){Style.RESET_ALL}\n")
        
        for path in paths:
            url = domain.rstrip('/') + path
            self.scan_url(url)
        
        self._show_summary()
    
    def _show_summary(self):
        """Show scan summary"""
        duration = time.time() - self.stats['start_time']
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] SCAN COMPLETE!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"Total URLs: {self.stats['total']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Redirects: {self.stats['redirects']}")
        print(f"Duration: {duration:.2f}s")
        print(f"Rate: {self.stats['total']/duration:.1f} URLs/sec")
        
        if self.stats['status_codes']:
            print(f"\n{Fore.CYAN}Status Codes:{Style.RESET_ALL}")
            for code, count in sorted(self.stats['status_codes'].items()):
                if code.startswith('2'):
                    color = Fore.GREEN
                elif code.startswith('3'):
                    color = Fore.YELLOW
                elif code.startswith('4'):
                    color = Fore.MAGENTA
                elif code.startswith('5'):
                    color = Fore.RED
                else:
                    color = Fore.WHITE
                print(f"  {color}{code}: {count}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}Results saved to: {self.output_dir}/results.jsonl{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Want more? Upgrade to FULL HTTPxray:{Style.RESET_ALL}")
        print(f"  • Technology Detection (50+ signatures)")
        print(f"  • Security Headers (20+ checks)")
        print(f"  • Sensitive Data (PII, secrets, keys)")
        print(f"  • CVE Scanning • WAF Detection • CMS Scanner")
        print(f"  • ML Anomaly Detection • REST API • Web Dashboard")
        print(f"  • HTML/PDF Reports • SQL/NoSQL Database")
        print(f"  • Distributed Scanning • Plugin System")
        print(f"\n{Fore.YELLOW}GitHub: https://github.com/ssecgroup/httpxray{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Donate ETH: 0x8242f0f25c5445F7822e80d3C9615e57586c6639{Style.RESET_ALL}")

# ==================== MAIN CLI ====================
def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='HTTPxray-Mini - Experience the power of HTTPxray!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
{Fore.CYAN}EXAMPLES:{Style.RESET_ALL}
  {Fore.GREEN}# Scan single URL{Style.RESET_ALL}
  python httpxray-mini.py -u https://example.com
  
  {Fore.GREEN}# Scan domain with common paths{Style.RESET_ALL}
  python httpxray-mini.py -d example.com --verbose
  
  {Fore.GREEN}# Scan list of URLs{Style.RESET_ALL}
  python httpxray-mini.py -l urls.txt --threads 10
  
  {Fore.GREEN}# Watch results live{Style.RESET_ALL}
  tail -f outputs/results.jsonl | jq '.status'
  
{Fore.CYAN}UPGRADE TO FULL VERSION:{Style.RESET_ALL}
  pip install httpxray[full]
  https://github.com/ssecgroup/httpxray
        '''
    )
    
    parser.add_argument('-u', '--url', help='Single URL to scan')
    parser.add_argument('-d', '--domain', help='Domain to scan')
    parser.add_argument('-l', '--list', help='File containing URLs')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-t', '--threads', type=int, default=5, help='Number of threads (default: 5)')
    parser.add_argument('-o', '--output', default='outputs', help='Output directory')
    parser.add_argument('--version', action='version', version=f'HTTPxray-Mini v{VERSION}')
    
    args = parser.parse_args()
    
    print(BANNER)
    
    # Validate input
    if not any([args.url, args.domain, args.list]):
        print(f"{Fore.RED}Error: No input provided. Use -u, -d, or -l{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Try: python httpxray-mini.py -u https://example.com{Style.RESET_ALL}")
        sys.exit(1)
    
    # Create scanner
    scanner = HTTPxrayMini(
        output_dir=args.output,
        verbose=args.verbose,
        threads=args.threads
    )
    
    # Run scan
    try:
        if args.url:
            scanner.scan_url(args.url)
            scanner._show_summary()
        elif args.domain:
            scanner.scan_domain(args.domain)
        elif args.list:
            scanner.scan_file(args.list)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scan interrupted{Style.RESET_ALL}")
        scanner._show_summary()
        sys.exit(130)

if __name__ == '__main__':
    main()
