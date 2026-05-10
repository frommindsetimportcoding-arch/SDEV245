"""Python-based CLI tool that scans files and directories for common patterns indicating hardcoded secrets."""
import re
import os 
import argparse
import logging

logger = logging.getLogger(__name__)


# Regex patterns for secrets. 
SECRET_PATTERNS = {
    'AWS IAM Access Key ID': r'AKIA[0-9A-Z]{16}',
    'Google API key': r'AIza[0-9A-Za-z-_]{35}',
    'Anthropic Claude': r'sk-ant-api03-[a-zA-Z0-9_\-]{93,}',
    'npm': r'npm_[A-Za-z0-9]{36}',
    'Webhook': r'T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}',
    'OpenAI': r'sk-proj-[A-Za-z0-9_\-]{48,}'
}

def scan_file(file_path, patterns):
    """ Scans the file for secret patterns."""
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for secret_type, pattern in patterns.items():
                    if re.search(pattern, line):
                        results.append({
                            'file': file_path,
                            'line': line_num,
                            'type': secret_type,
                            'match': line.strip()
                        })
    except Exception as e:
        logger.error(f'Could not read {file_path}: {e}')
    return results


def setup_logging(verbose):
    """
    Configures logging based on verbose flag.
    If --verbose is used, set level to DEBUG; otherwise, use INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format='%(name)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S', force=True) # could add filename='scanner.log', filemode='a' for append ='w' for write


def scanner():
    """Parses """
    parser = argparse.ArgumentParser(description='Scan files for hardcoded secrets.')
    parser.add_argument('path', help='File or directory to scan')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    setup_logging(args.verbose)

    target = args.path
    all_results = []

    logger.info(f'Target path: {target}')

    if args.verbose:
        logger.debug('Verbose mode enabled. Detailed file tracking active.')


    if os.path.isfile(target):
        all_results.extend(scan_file(target, SECRET_PATTERNS))
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            # Adding this line of code to whitelist common text/code formats that secrets would live in.
            VALID_EXTENSIONS = ('.py', '.env', '.txt', '.json', '.yml', '.yaml', '.js', '.conf')

            for file in files:
                if file.endswith(VALID_EXTENSIONS):

                    file_path = os.path.join(root, file)
                    logger.debug(f'Scanning file: {file_path}')
                    all_results.extend(scan_file(file_path, SECRET_PATTERNS))
    else:
        logging.error('Invalid path.')
        return
    
    if all_results:
        print(f'\nFound {len(all_results)} potential secrets:\n')
        for r in all_results:
            print(f'File: {r['file']} (Line {r['line']})')
            print(f'Type: {r['type']}')
            print(f'Match: {r['match']}\n')
    else:
        print('No secrets found.')


if __name__ == '__main__':
    scanner()


