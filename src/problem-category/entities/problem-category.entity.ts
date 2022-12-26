import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';
@Entity()
export class ProblemCategory {
  @PrimaryGeneratedColumn('increment')
  id: number;
  @Column()
  name: string;
  @Column()
  problem_types: string;
}
