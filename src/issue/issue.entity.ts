import {
  BaseEntity,
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
  Relation,
} from 'typeorm';


@Entity()
export class Issue extends BaseEntity {
   
  @PrimaryGeneratedColumn('uuid')
  id: string;
  @Column()
  requester: string;
  @Column()
  phone: string;
  @Column()
  city: string;
  @Column()
  workstation: string;
  @Column()
  problem_category: string;
  @Column()
  problem_type: string;
  @Column()
  email: string;

  @Column()
  date: Date;
  
}
