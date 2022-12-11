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
export class Chamado extends BaseEntity {
   
  @PrimaryGeneratedColumn('uuid')
  id: string;
  @Column()
  solicitante: string;
  @Column()
  telefone: string;
  @Column()
  cidade: string;
  @Column()
  posto_trabalho: string;
  @Column()
  categoria_problema: string;
  @Column()
  tipo_problema: string;
  @Column()
  email: string;

  @Column()
  date: Date;
  
}
