import { DataSource } from 'typeorm';
import { ConfigService } from '@nestjs/config';
import { Teste1670639446869 } from './migrations/1670639446869-Teste';
import { Relation1670730610205 } from './migrations/1670730610205-Relation';

const configService = new ConfigService();

export default new DataSource({
  type: 'postgres',
  host: 'localhost',
  port: 5105,
  username: 'postgres',
  password: 'postgres',
  database: 'schedula_core',
  entities: ['./src/**/*.entity.ts'],
  migrations: [Teste1670639446869, Relation1670730610205],
});
