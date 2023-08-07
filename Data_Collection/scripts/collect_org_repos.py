# to run this file
# python collect_org_repos.py pik-piam --access_token your_access_token

import argparse
import requests
import csv

def get_all_repositories(org_name, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/orgs/{org_name}/repos"

    all_repositories = []
    page = 1
    per_page = 100

    while True:
        params = {
            "page": page,
            "per_page": per_page
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error occurred: {response.status_code}")
            break

        repositories = response.json()
        all_repositories.extend(repositories)

        if len(repositories) < per_page:
            break

        page += 1

    return all_repositories

def save_to_csv(repositories, org_name):
    keys = ["name", "owner", "description", "language", "forks_count", "stargazers_count", 'events_url', 'tags_url',
            'private', 'notifications_url', 'blobs_url', 'deployments_url', 'keys_url', 'archived', 'ssh_url',
            'watchers', 'forks', 'contributors_url', 'releases_url', 'id', 'disabled', 'permissions', 'languages_url',
            'git_commits_url', 'visibility', 'labels_url', 'fork', 'trees_url', 'mirror_url', 'is_template',
            'web_commit_signoff_required', 'issue_events_url', 'subscription_url', 'stargazers_url', 'git_url',
            'node_id', 'commits_url', 'subscribers_url', 'allow_forking', 'default_branch', 'has_downloads',
            'assignees_url', 'comments_url', 'full_name', 'hooks_url', 'collaborators_url', 'contents_url',
            'statuses_url', 'html_url', 'size', 'issue_comment_url', 'milestones_url', 'open_issues', 'watchers_count',
            'git_refs_url', 'license', 'issues_url', 'svn_url', 'has_wiki', 'archive_url', 'has_issues',
            'open_issues_count', 'downloads_url', 'pulls_url', 'owner', 'url', 'homepage', 'topics', 'created_at',
            'clone_url', 'merges_url', 'branches_url', 'updated_at', 'git_tags_url', 'has_pages', 'forks_url',
            'pushed_at', 'teams_url', 'has_projects', 'has_discussions', 'compare_url']

    with open(filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(repositories)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Organization Repositories to CSV")
    parser.add_argument("org_name", type=str, help="Name of the GitHub organization")
    parser.add_argument("--access_token", type=str, default="", help="Your GitHub access token")
    args = parser.parse_args()

    access_token = args.access_token
    org_name = args.org_name
    filename = f"results/{org_name}_repositories.csv"

    repositories = get_all_repositories(org_name, access_token)
    save_to_csv(repositories, org_name)
    print(f"Repositories saved to {filename}.")
