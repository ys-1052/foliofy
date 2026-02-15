import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { FoliofyStack } from '../lib/foliofy-stack';

describe('FoliofyStack', () => {
  let app: cdk.App;
  let stack: FoliofyStack;
  let template: Template;

  beforeEach(() => {
    app = new cdk.App();
    stack = new FoliofyStack(app, 'TestStack', {
      env: {
        account: '123456789012',
        region: 'ap-northeast-1',
      },
    });
    template = Template.fromStack(stack);
  });

  test('should create Cognito User Pool', () => {
    template.hasResourceProperties('AWS::Cognito::UserPool', {
      UserPoolName: 'foliofy-user-pool',
      AutoVerifiedAttributes: ['email'],
      UsernameAttributes: ['email'],
      Policies: {
        PasswordPolicy: {
          MinimumLength: 8,
          RequireLowercase: true,
          RequireUppercase: true,
          RequireNumbers: true,
          RequireSymbols: false,
        },
      },
    });
  });

  test('should create Cognito User Pool Client', () => {
    template.hasResourceProperties('AWS::Cognito::UserPoolClient', {
      ClientName: 'foliofy-web-client',
      ExplicitAuthFlows: [
        'ALLOW_USER_PASSWORD_AUTH',
        'ALLOW_USER_SRP_AUTH',
        'ALLOW_REFRESH_TOKEN_AUTH',
      ],
      GenerateSecret: false,
      PreventUserExistenceErrors: 'ENABLED',
    });
  });

  test('should have User Pool with email self-signup enabled', () => {
    template.hasResourceProperties('AWS::Cognito::UserPool', {
      AdminCreateUserConfig: {
        AllowAdminCreateUserOnly: false,
      },
    });
  });

  test('should have User Pool with RETAIN deletion policy', () => {
    template.hasResource('AWS::Cognito::UserPool', {
      DeletionPolicy: 'Retain',
      UpdateReplacePolicy: 'Retain',
    });
  });

  test('should output UserPoolId', () => {
    template.hasOutput('UserPoolId', {
      Description: 'Cognito User Pool ID',
    });
  });

  test('should output UserPoolClientId', () => {
    template.hasOutput('UserPoolClientId', {
      Description: 'Cognito User Pool Client ID',
    });
  });

  test('should output UserPoolArn', () => {
    template.hasOutput('UserPoolArn', {
      Description: 'Cognito User Pool ARN',
    });
  });

  test('should create exactly one User Pool', () => {
    template.resourceCountIs('AWS::Cognito::UserPool', 1);
  });

  test('should create exactly one User Pool Client', () => {
    template.resourceCountIs('AWS::Cognito::UserPoolClient', 1);
  });

  test('snapshot test - CloudFormation template should match', () => {
    expect(template.toJSON()).toMatchSnapshot();
  });
});
