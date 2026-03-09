pipeline{
    agent any

     environment {
        SONAR_PROJECT_KEY = 'LLMOPs'
	 	SONAR_SCANNER_HOME = tool 'sonarqube_scanner'
    //     AWS_REGION = 'ap-south-1'
    //     ECR_REPO = 'llmops-ecr'
    //     IMAGE_TAG = 'latest'
	 }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'LLMOPS', url: 'https://github.com/vujwal4/Multi-LLMOPS-using-bedrock.git']])
                }
            }
        }

        stage('SonarQube Analysis'){
        		steps {
        			withCredentials([string(credentialsId: 'sonarqube_token', variable: 'SONAR_TOKEN')]) {
                            
        				withSonarQubeEnv('sonar_env') {
        						sh """
        					${SONAR_SCANNER_HOME}/bin/sonar-scanner \
        					-Dsonar.projectKey=${SONAR_PROJECT_KEY} \
        					-Dsonar.sources=. \
        					-Dsonar.host.url=http://sonarqube-jin:9000 \
        					-Dsonar.login=${SONAR_TOKEN}
        					"""
        				}
        			}
        		}
        	}

    // stage('Build and Push Docker Image to ECR') {
    //         steps {
    //             withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
    //                 script {
    //                     def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
    //                     def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"

    //                     sh """
    //                     aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
    //                     docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
    //                     docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}
    //                     docker push ${ecrUrl}:${IMAGE_TAG}
    //                     """
    //                 }
    //             }
    //         }
    //     }

    //     stage('Deploy to ECS Fargate') {
    // steps {
    //     withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
    //         script {
    //             sh """
    //             aws ecs update-service \
    //               --cluster multi-llmops-pip \
    //               --service llmops-task-def-service-n5eo72vv  \
    //               --force-new-deployment \
    //               --region ${AWS_REGION}
    //             """
    //             }
    //         }
    //     }
    //  }
        
    }
}