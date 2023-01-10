import { DataSourceOptions } from 'typeorm';
import configuration from 'src/configs/configuration';

const configService = configuration();

export const config: DataSourceOptions = {
  type: 'postgres',
  host: configService.database.host,
  port: configService.database.port,
  username: configService.database.user,
  password: configService.database.pass,
  database: configService.database.db,
  synchronize: true, // Obs: use synchronize: true somente em desenvolvimento.
  entities: ['./src/**/*.entity.ts'],
};
