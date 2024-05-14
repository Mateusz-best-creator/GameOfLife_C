#pragma once

#include "animal.hpp"

class Human : public Animal
{
private:
    static int HUMAN_STATIC_COUNTER;
    bool ability_activated;
    int ability_counter;
    int normal_strength;

public:
    Human(int, int);
    Human(int, int, int, int, int, bool, int);
    ~Human();

    virtual ActionResult action(std::vector<std::vector<char>>&) override final;
    virtual CollisionResult collision(std::vector<std::vector<char>>&, std::vector<Organism*>&, int) override final;
    virtual int get_static_counter() override final;
};