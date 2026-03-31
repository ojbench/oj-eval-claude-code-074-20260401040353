#!/usr/bin/env python3
"""
ACMOJ Submission Client
Submits git repository URL to ACMOJ and checks submission status
"""

import os
import sys
import json
import time
import requests
import argparse

ACMOJ_API_BASE = "https://acm.sjtu.edu.cn/OnlineJudge/api"

def get_token():
    """Get ACMOJ token from environment"""
    token = os.environ.get('ACMOJ_TOKEN')
    if not token:
        print("ERROR: ACMOJ_TOKEN environment variable not set")
        sys.exit(1)
    return token

def get_problem_id():
    """Get problem ID from environment"""
    problem_id = os.environ.get('ACMOJ_PROBLEM_ID')
    if not problem_id:
        print("ERROR: ACMOJ_PROBLEM_ID environment variable not set")
        sys.exit(1)
    return problem_id

def submit(repo_url, branch='main'):
    """Submit git repository to ACMOJ"""
    token = get_token()
    problem_id = get_problem_id()

    print(f"Submitting to ACMOJ...")
    print(f"Problem ID: {problem_id}")
    print(f"Repository: {repo_url}")
    print(f"Branch: {branch}")

    # Try multiple API formats
    api_endpoints = [
        ("https://acm.sjtu.edu.cn/api/judge/submit", {
            'X-Auth-Token': token,
            'Content-Type': 'application/json'
        }, {
            'problem_id': int(problem_id),
            'type': 'git',
            'git_url': repo_url,
            'git_branch': branch
        }),
        (f"https://acm.sjtu.edu.cn/api/problems/{problem_id}/submit", {
            'X-Auth-Token': token,
            'Content-Type': 'application/json'
        }, {
            'repo_url': repo_url,
            'branch': branch,
            'language': 'verilog'
        }),
        (f"{ACMOJ_API_BASE}/submit", {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }, {
            'problem_id': problem_id,
            'repo_url': repo_url,
            'branch': branch,
            'language': 'verilog'
        }),
    ]

    for endpoint, headers, data in api_endpoints:
        try:
            print(f"\nTrying endpoint: {endpoint}")
            response = requests.post(
                endpoint,
                headers=headers,
                json=data,
                timeout=30,
                allow_redirects=False
            )

            print(f"Status code: {response.status_code}")

            if response.status_code == 200:
                try:
                    result = response.json()
                    submission_id = result.get('submission_id') or result.get('id')
                    print(f"\n✓ Submission successful!")
                    print(f"Submission ID: {submission_id}")
                    print(f"\nUse this command to check status:")
                    print(f"  python3 submit_acmoj/acmoj_client.py status {submission_id}")
                    return submission_id
                except:
                    print(f"Response: {response.text[:200]}")
            elif response.status_code == 201:
                try:
                    result = response.json()
                    submission_id = result.get('submission_id') or result.get('id')
                    print(f"\n✓ Submission successful!")
                    print(f"Submission ID: {submission_id}")
                    return submission_id
                except:
                    print(f"Response: {response.text[:200]}")
                    return "created"
            else:
                print(f"Response preview: {response.text[:200]}")

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            continue

    print(f"\n✗ All submission attempts failed!")
    print(f"\nThe repository has been pushed to: {repo_url}")
    print(f"The OJ system may pick it up automatically.")
    return None

def check_status(submission_id):
    """Check status of a submission"""
    token = get_token()

    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.get(
            f"{ACMOJ_API_BASE}/submission/{submission_id}",
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            status = result.get('status', 'Unknown')
            score = result.get('score', 0)
            message = result.get('message', '')

            print(f"\nSubmission ID: {submission_id}")
            print(f"Status: {status}")
            print(f"Score: {score}")
            if message:
                print(f"Message: {message}")

            # Show detailed results if available
            if 'test_cases' in result:
                print("\nTest Case Results:")
                for tc in result['test_cases']:
                    tc_name = tc.get('name', 'Unknown')
                    tc_status = tc.get('status', 'Unknown')
                    tc_score = tc.get('score', 0)
                    print(f"  {tc_name}: {tc_status} (score: {tc_score})")

            return result
        else:
            print(f"\n✗ Failed to get status!")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"\n✗ Request error: {e}")
        return None

def abort_submission(submission_id):
    """Abort a pending submission"""
    token = get_token()

    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.post(
            f"{ACMOJ_API_BASE}/submission/{submission_id}/abort",
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            print(f"\n✓ Submission {submission_id} aborted successfully!")
            print("Note: Aborted submissions do NOT count toward your submission limit.")
            return True
        else:
            print(f"\n✗ Failed to abort submission!")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"\n✗ Request error: {e}")
        return False

def list_submissions():
    """List all submissions for the current problem"""
    token = get_token()
    problem_id = get_problem_id()

    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.get(
            f"{ACMOJ_API_BASE}/submissions?problem_id={problem_id}",
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            submissions = response.json()
            print(f"\nSubmissions for Problem {problem_id}:")
            print("-" * 80)
            for sub in submissions:
                sub_id = sub.get('submission_id')
                status = sub.get('status')
                score = sub.get('score', 0)
                timestamp = sub.get('timestamp', '')
                print(f"ID: {sub_id} | Status: {status} | Score: {score} | Time: {timestamp}")
            return submissions
        else:
            print(f"\n✗ Failed to list submissions!")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"\n✗ Request error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='ACMOJ Submission Client')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Submit command
    submit_parser = subparsers.add_parser('submit', help='Submit repository to ACMOJ')
    submit_parser.add_argument('repo_url', help='Git repository URL')
    submit_parser.add_argument('--branch', default='main', help='Branch name (default: main)')

    # Status command
    status_parser = subparsers.add_parser('status', help='Check submission status')
    status_parser.add_argument('submission_id', help='Submission ID to check')

    # Abort command
    abort_parser = subparsers.add_parser('abort', help='Abort a pending submission')
    abort_parser.add_argument('submission_id', help='Submission ID to abort')

    # List command
    list_parser = subparsers.add_parser('list', help='List all submissions')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'submit':
        submit(args.repo_url, args.branch)
    elif args.command == 'status':
        check_status(args.submission_id)
    elif args.command == 'abort':
        abort_submission(args.submission_id)
    elif args.command == 'list':
        list_submissions()

if __name__ == '__main__':
    main()
