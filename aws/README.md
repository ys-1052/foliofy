# Foliofy AWS Infrastructure

AWS CDK for Cognito User Pool

## Setup

```bash
npm install
```

## Deploy with AWS Profile

### Method 1: Environment variable

```bash
AWS_PROFILE=your-profile npm run deploy
AWS_PROFILE=your-profile npm run synth
AWS_PROFILE=your-profile npm run diff
```

### Method 2: Direct CDK command

```bash
npx cdk deploy --profile your-profile
npx cdk bootstrap --profile your-profile
```

## Deploy without Profile

```bash
npm run deploy
```

## Outputs

After deployment, note these values:
- `UserPoolId` - Add to backend `.env`
- `UserPoolClientId` - Add to backend `.env`
- `UserPoolArn` - For reference
