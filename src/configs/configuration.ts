export default () => ({
  database: {
    host: process.env.DATABASE_HOST,
    user: process.env.DATABASE_USER,
    pass: process.env.DATABASE_PASS,
    db: process.env.DATABASE_DB,
    address: 'schedula_core_db',
    port: parseInt(process.env.DATABASE_PORT) || 5105,
  },
  environment: process.env.ENVIRONMENT,
});
