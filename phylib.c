#include "phylib.h"


// This function creates a new still ball object with the specified number and position.
// It allocates memory for the object and initializes its type, number, and position.
phylib_object *phylib_new_still_ball( unsigned char number,phylib_coord *pos )  {

    phylib_object *object = (phylib_object *)malloc(sizeof(phylib_object));

    if (object == NULL) {
        return NULL;
    }

    object -> type = PHYLIB_STILL_BALL;
    object -> obj.still_ball.number = number; 
    object -> obj.still_ball.pos = *pos; 

    return object;

}

// This function creates a new rolling ball object with the specified number, position, velocity, and acceleration.
// It allocates memory for the object and initializes its type, number, position, velocity, and acceleration.
phylib_object *phylib_new_rolling_ball( unsigned char number,phylib_coord *pos,phylib_coord *vel,phylib_coord *acc )  {

    phylib_object *object = (phylib_object *)malloc(sizeof(phylib_object));

    if (object == NULL) {
        return NULL;
    }

    object -> type = PHYLIB_ROLLING_BALL;
    object -> obj.rolling_ball.number = number;
    object -> obj.rolling_ball.pos = *pos;
    object -> obj.rolling_ball.vel = *vel;
    object -> obj.rolling_ball.acc = *acc;

    return object;
 
}

// This function creates a new hole object with the specified position.
// It allocates memory for the object and initializes its type and position.
phylib_object *phylib_new_hole( phylib_coord *pos )  {

    phylib_object *object = (phylib_object *)malloc(sizeof(phylib_object));

    if (object == NULL) {
        return NULL;
    }

    object -> type = PHYLIB_HOLE;
    object -> obj.hole.pos = *pos; 

    return object;

}

// This function creates a new horizontal cushion object with the specified position.
// It allocates memory for the object and initializes its type and position.
phylib_object *phylib_new_hcushion( double y )  {

    phylib_object *object = (phylib_object *)malloc(sizeof(phylib_object));

    if (object == NULL) {
        return NULL;
    }

    object -> type = PHYLIB_HCUSHION;
    object -> obj.hcushion.y = y; 

    return object;

}

// This function creates a new vertical cushion object with the specified position.
// It allocates memory for the object and initializes its type and position.
phylib_object *phylib_new_vcushion( double x )  {

    phylib_object *object = (phylib_object *)malloc(sizeof(phylib_object));

    if (object == NULL) {
        return NULL;
    }

    object -> type = PHYLIB_VCUSHION;
    object -> obj.vcushion.x = x; 

    return object;
}

// This function creates a new table with predefined objects such as cushions and holes.
// It allocates memory for the table and initializes its time and objects.
phylib_table *phylib_new_table( void )  {

    phylib_table *table = (phylib_table *)malloc(sizeof(phylib_table));

    if (table == NULL) {
        return NULL;
    }

    phylib_coord pos;

    table -> time = 0.0;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        table->object[i] = NULL;
    }

    // Initialize objects representing cushions and holes
    table -> object[0] = phylib_new_hcushion(0.0);
    table -> object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    table -> object[2] = phylib_new_vcushion(0.0);
    table -> object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // Create holes at the corners of the table
    pos.x = 0.0, pos.y = 0.0;
    table -> object[4] = phylib_new_hole(&pos);

    pos.x = 0.0, pos.y = PHYLIB_TABLE_WIDTH;
    table -> object[5] = phylib_new_hole(&pos);

    pos.x = 0.0, pos.y = PHYLIB_TABLE_LENGTH;
    table -> object[6] = phylib_new_hole(&pos);

    pos.x = PHYLIB_TABLE_WIDTH, pos.y = 0.0;
    table -> object[7] = phylib_new_hole(&pos);

    pos.x = PHYLIB_TABLE_WIDTH, pos.y = PHYLIB_TABLE_WIDTH;
    table -> object[8] = phylib_new_hole(&pos);

    pos.x = PHYLIB_TABLE_WIDTH, pos.y = PHYLIB_TABLE_LENGTH;
    table -> object[9] = phylib_new_hole(&pos);

    return table;
}

// This function creates a copy of an object and assigns it to a destination pointer.
void phylib_copy_object( phylib_object **dest, phylib_object **src )  {
    if (*src == NULL) {
        *dest = NULL;
        return;
    }

    *dest = (phylib_object *)malloc(sizeof(phylib_object));

    if (*dest == NULL) {
        return;
    }

    memcpy(*dest, *src, sizeof(phylib_object));

}

// This function creates a copy of a table, including its objects and time.
phylib_table *phylib_copy_table( phylib_table *table )  {

    if (table == NULL) {
        return NULL;
    }

    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));

    if (newTable == NULL) {
        return NULL;  
    }

    // Copy objects and time from the original table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
    }

    newTable->time = table->time;

    return newTable;
}

// This function adds an object to a table.
void phylib_add_object( phylib_table *table, phylib_object *object )  {

    if (table == NULL || object == NULL) {
        return;
    }

    // Find an empty slot in the table and add the object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)  {
        if (table -> object[i] == NULL)  {
            table -> object[i] = object;
            return;
        }
    }
}

// This function frees the memory occupied by a table and its objects.
void phylib_free_table( phylib_table *table )  {

    if (table == NULL) {
        return;
    }

    // Free memory occupied by each object in the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)  {
        if (table -> object[i] != NULL)  {
            free(table -> object[i]);
            table->object[i] = NULL;
        }
    }

    free(table);

}

// This function calculates the difference between two coordinates.
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 )  {
    phylib_coord result;

    result.x = 0.0;
    result.y = 0.0;

    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;

    return result;
}

// This function calculates the length of a coordinate vector.
double phylib_length( phylib_coord c )  {
    
    double length = 0.0;
    length = sqrt((c.x*c.x)+(c.y*c.y));

    return length;
}

// This function calculates the dot product of two coordinate vectors.
double phylib_dot_product( phylib_coord a, phylib_coord b )  {
    double product = 0.0;
    product = (a.x*b.x) + (a.y*b.y);

    return product;
}

// This function calculates the distance between two objects.
double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1;
    }

    double distance = 0.0;
    double dx = 0.0, dy = 0.0;

    if (obj2->type == PHYLIB_ROLLING_BALL) {
        dx = obj2->obj.rolling_ball.pos.x - obj1->obj.rolling_ball.pos.x;
        dy = obj2->obj.rolling_ball.pos.y - obj1->obj.rolling_ball.pos.y;
        distance = sqrt(dx * dx + dy * dy) - PHYLIB_BALL_DIAMETER;

    } else if (obj2->type == PHYLIB_STILL_BALL) {
        dx = obj2->obj.rolling_ball.pos.x - obj1->obj.rolling_ball.pos.x;
        dy = obj2->obj.rolling_ball.pos.y - obj1->obj.rolling_ball.pos.y;
        distance = sqrt(dx * dx + dy * dy) - PHYLIB_BALL_DIAMETER;

    } else if (obj2->type == PHYLIB_HOLE) {
        dx = obj2->obj.hole.pos.x - obj1->obj.rolling_ball.pos.x;
        dy = obj2->obj.hole.pos.y - obj1->obj.rolling_ball.pos.y;
        distance = sqrt(dx * dx + dy * dy) - PHYLIB_HOLE_RADIUS;

    } else if (obj2->type == PHYLIB_HCUSHION) {
        distance = fabs(obj2->obj.hcushion.y - obj1->obj.rolling_ball.pos.y) - PHYLIB_BALL_RADIUS;

    } else if (obj2->type == PHYLIB_VCUSHION) {
        distance = fabs(obj2->obj.vcushion.x - obj1->obj.rolling_ball.pos.x) - PHYLIB_BALL_RADIUS;
        
    } else {
        return -1;
    }
    return distance;
}


// This function updates the position, velocity, and acceleration of a rolling ball object over time.
void phylib_roll( phylib_object *new, phylib_object *old, double time )  {

    if (new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
        return;
    }
    double new_x_pos = 0.0;
    double new_y_pos = 0.0;
    double new_x_vel = 0.0;
    double new_y_vel = 0.0;

    // Calculate new position using kinematic equations
    new_x_pos = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time +
                       0.5 * old->obj.rolling_ball.acc.x * time * time;
    new_y_pos = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time +
                       0.5 * old->obj.rolling_ball.acc.y * time * time;
                       
    new->obj.rolling_ball.pos.x = new_x_pos;
    new->obj.rolling_ball.pos.y = new_y_pos;

    // Update velocity using acceleration
    new_x_vel = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    new_y_vel = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;


    new->obj.rolling_ball.vel.x = new_x_vel;
    new->obj.rolling_ball.vel.y = new_y_vel;

    // Preserve acceleration from the old object
    new->obj.rolling_ball.acc.x = old->obj.rolling_ball.acc.x;
    new->obj.rolling_ball.acc.y = old->obj.rolling_ball.acc.y;

    // If the ball changes direction, reset velocity and acceleration components to prevent overshooting
    if (old->obj.rolling_ball.vel.x * new->obj.rolling_ball.vel.x < 0.0){
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;

    }

    if (old->obj.rolling_ball.vel.y * new->obj.rolling_ball.vel.y < 0.0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }

}

// This function checks if a rolling ball has stopped moving and converts it to a still ball.
unsigned char phylib_stopped( phylib_object *object )  {
    if (object->type != PHYLIB_ROLLING_BALL) {
        return 0;
    }

    double speed = 0.0;
    speed = phylib_length(object->obj.rolling_ball.vel);

    // If the speed is below a threshold, convert the object to a still ball
    if (speed < PHYLIB_VEL_EPSILON) {
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;
        object->obj.still_ball.number = object->obj.rolling_ball.number;

        return 1;
    }

    return 0;
}  

// This function handles the collision between two objects.
void phylib_bounce( phylib_object **a, phylib_object **b )  {
    phylib_coord r_ab ;
    r_ab.x = 0.0, r_ab.y = 0.0;

    phylib_coord v_rel;
    v_rel.x = 0.0, v_rel.y = 0.0;

    phylib_coord n;
    n.x = 0.0, n.y = 0.0;

    double v_rel_n = 0.0;
    double speed_a = 0.0;
    double speed_b = 0.0;

    if (*a == NULL || *b == NULL) {
        return;
    }

    if ((*a)->type != PHYLIB_ROLLING_BALL) {
        return;
    }

    switch((*b)->type)  {
            // Handle collision with horizontal cushion by reversing y velocity and acceleration
            case PHYLIB_HCUSHION:
                (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
                (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
                break;

            // Handle collision with vertical cushion by reversing x velocity and acceleration
            case PHYLIB_VCUSHION:
                (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
                (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
                break;

            // Remove the ball if it falls into a hole
            case PHYLIB_HOLE:
                free(*a);
                (*a) = NULL;
                break;

            // Convert a rolling ball to a still ball if it collides with another still ball
            case PHYLIB_STILL_BALL:
                (*b)->type = PHYLIB_ROLLING_BALL;
                (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
                (*b)->obj.rolling_ball.pos.x = (*b)->obj.still_ball.pos.x;
                (*b)->obj.rolling_ball.pos.y = (*b)->obj.still_ball.pos.y;

                (*b)->obj.rolling_ball.vel.x = 0.0;
                (*b)->obj.rolling_ball.vel.y = 0.0;

                (*b)->obj.rolling_ball.acc.x = 0.0;
                (*b)->obj.rolling_ball.acc.y = 0.0;
                // Intentional fallthrough to handle collision with another rolling ball

            case PHYLIB_ROLLING_BALL:
                
                r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
                v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);


                n.x = r_ab.x / phylib_length(r_ab);
                n.y = r_ab.y / phylib_length(r_ab);

                v_rel_n = phylib_dot_product(v_rel,n);
                
                (*a)->obj.rolling_ball.vel.x -= (v_rel_n * n.x); 
                (*a)->obj.rolling_ball.vel.y -= (v_rel_n * n.y); 

                (*b)->obj.rolling_ball.vel.x += (v_rel_n * n.x); 
                (*b)->obj.rolling_ball.vel.y += (v_rel_n * n.y); 

                speed_a = phylib_length((*a)->obj.rolling_ball.vel);
                speed_b = phylib_length((*b)->obj.rolling_ball.vel);

                // Apply drag if the ball is moving
                if(speed_a > PHYLIB_VEL_EPSILON) {
                    (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.vel.x * -1.0 / speed_a * PHYLIB_DRAG;
                    (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.vel.y * -1.0 / speed_a * PHYLIB_DRAG;
                }

                if(speed_b > PHYLIB_VEL_EPSILON) {
                    (*b)->obj.rolling_ball.acc.x = (*b)->obj.rolling_ball.vel.x * -1.0 / speed_b * PHYLIB_DRAG;
                    (*b)->obj.rolling_ball.acc.y = (*b)->obj.rolling_ball.vel.y * -1.0 / speed_b * PHYLIB_DRAG;
                    
                }

                break;

            default:
                break;
    }

}

// This function counts the number of rolling balls on the table.
unsigned char phylib_rolling(phylib_table *t) {
    int count = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            count++;
        }
    }

    return count;
}

// This function segments the simulation time and handles object interactions.
phylib_table *phylib_segment(phylib_table *table) {
    if (phylib_rolling(table) == 0) {
        return NULL;
    }

    phylib_table *new = phylib_copy_table(table);
    double time = 0.0;
    time = table->time + PHYLIB_SIM_RATE;

    while (time < PHYLIB_MAX_TIME) {
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (new->object[i] && new->object[i]->type == PHYLIB_ROLLING_BALL) {
                phylib_roll(new->object[i], new->object[i], PHYLIB_SIM_RATE); 
                if (phylib_stopped(new->object[i])) {
                    new->time = time; 
                    return new;
                }
            }
        }

        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                if (i != j && new->object[i] && new->object[j] && new->object[i]->type == PHYLIB_ROLLING_BALL &&  phylib_distance(new->object[i], new->object[j]) < 0.0) {
                    phylib_bounce(&new->object[i], &new->object[j]);
                    new->time = time; 
                    return new;
                }
            }
        }
        
    
        time += PHYLIB_SIM_RATE; 
        new->time = time; 
    }

    return new;
}

char *phylib_object_string( phylib_object *object )
{
    static char string[80];

    if (object==NULL)  {
        snprintf( string, 80, "NULL;" );
        return string;
    }

    switch (object->type)  {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;

        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
        
        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;

        case PHYLIB_HCUSHION:
            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
            break;
    }
    return string;
}
