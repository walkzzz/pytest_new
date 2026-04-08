"""
Jenkins 自动配置脚本 - 使用API Key认证
"""

import jenkins
import time
import os

JENKINS_URL = "http://localhost:8080"
USERNAME = "admin"
PASSWORD = "3996517961304343abf6d5ef7631672a"  # initialAdminPassword

server = jenkins.Jenkins(JENKINS_URL, username=USERNAME, password=PASSWORD)

print(f"连接 Jenkins: {JENKINS_URL}")
time.sleep(2)

try:
    print(f"版本: {server.get_version()}")
except Exception as e:
    print(f"连接失败: {e}")
    exit(1)

print("\n=== 1. 创建 Pipeline Job ===")
pipeline_script = """pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat 'python -m pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat 'python -m pytest tests/ -v --tb=short'
            }
        }
    }
    post {
        always {
            junit '**/test-results/*.xml'
            archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true
        }
    }
}"""

try:
    server.create_job("pytest-pipeline", pipeline_script)
    print("✓ Pipeline Job 创建成功")
except Exception as e:
    print(f"创建失败: {e}")

print("\n=== 2. 创建 Freestyle Job ===")
freestyle_config = """<?xml version='1.1' encoding='UTF-8'?>
<project>
  <description>Pytest UI Automation Project</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class='hudson.scm.NullSCM'/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>python -m pip install -r requirements.txt && python -m pytest tests/ -v</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <junit.JUnitResultArchiver>
      <testResults>**/test-results/*.xml</testResults>
      <keepLongStdio>false</keepLongStdio>
      <healthScaleFactor>1.0</healthScaleFactor>
      <allowEmptyResults>false</allowEmptyResults>
    </junit.JUnitResultArchiver>
  </publishers>
  <buildWrappers/>
</project>"""

try:
    server.create_job("pytest-freestyle", freestyle_config)
    print("✓ Freestyle Job 创建成功")
except Exception as e:
    print(f"创建失败: {e}")

print("\n=== 3. 获取所有 Jobs ===")
try:
    jobs = server.get_jobs()
    for job in jobs:
        print(f"  - {job['name']}")
except Exception as e:
    print(f"获取Jobs失败: {e}")

print("\n=== 完成! ===")
print(f"访问 Jenkins: {JENKINS_URL}")
print(f"用户名: {USERNAME}")
print(f"密码: {PASSWORD}")
