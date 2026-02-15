#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { FoliofyStack } from '../lib/foliofy-stack';

const app = new cdk.App();
new FoliofyStack(app, 'FoliofyStack', {
  env: {
    account: '772786611036',
    region: 'ap-northeast-1',
  },
});
