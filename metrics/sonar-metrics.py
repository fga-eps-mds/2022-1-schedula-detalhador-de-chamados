from datetime import datetime
import sys
import urllib.request, json

def generate_metrics():
  base_url = "https://sonarcloud.io/api/measures/component_tree?component=fga-eps-mds_"
  prefix = "fga-eps-mds"
  metrics = [
    "files",
    "functions",
    "complexity",
    "comment_lines_density",
    "duplicated_lines_density",
    "coverage",
    "ncloc",
    "tests",
    "test_errors",
    "test_failures",
    "test_execution_time",
    "security_rating"
  ]

  # NAO RELE A MÃO NISSO AQUI
  repository_name = sys.argv[1]
  repository_version = sys.argv[2]
  underlined_repo_name = repository_name[:16] + repository_name[16:].replace('-', "_")
  url = base_url + repository_name + f"&metricKeys={','.join(metrics)}"
  with urllib.request.urlopen(url) as res:
    data = json.load(res)
    date = datetime.now()
    date_padrao_hilmer = f"{date.month}-{date.day}-{date.year}-{date.hour}-{date.minute}-{date.second}"
    
    filename = f"{prefix}-{underlined_repo_name}-{date_padrao_hilmer}-{repository_version}.json"
    print(filename)
    with open(filename, "w") as file:
      json.dump(data, file)

if __name__ == "__main__":
  generate_metrics()