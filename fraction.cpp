#include <iostream>
#include <stdexcept>

class Fraction {
private:
    long long num = 0;
    long long den = 1;

    static inline long long gcf(long long a, long long b) {
        a %= b;
        if (a < 0) a = -a;
        while (b != 0) {
            long long r = a % b;
            a = b;
            b = r;
        }
        return a;
    }

    void normalizeSign() {
        if (den < 0) {
            den = -den;
            num = -num;
        }
    }

public:
    // Constructors
    Fraction() : num(0), den(1) {}

    Fraction(long long val) : num(val), den(1) {}

    Fraction(long long n, long long d) : num(n), den(d) {
        if (d == 0)
            throw std::invalid_argument("Denominator cannot be zero");
        simplify();
    }

    // Methods
    Fraction& simplify() {
        normalizeSign();

        long long factor = gcf(num, den);
        num /= factor;
        den /= factor;

        return *this;
    }

    Fraction simplified() const {
        long long n = num, d = den;

        if (d < 0) {
            d = -d;
            n = -n;
        }

        long long factor = gcf(n, d);
        return Fraction(n / factor, d / factor);
    }

    //#######################################################
    //############## Operators
    //#######################################################
    Fraction operator+(Fraction const& other) const {
        return Fraction(num * other.den + other.num * den,
                        den * other.den);
    }

    Fraction operator-(Fraction const& other) const {
        return Fraction(num * other.den - other.num * den,
                        den * other.den);
    }

    Fraction operator*(Fraction const& other) const {
        return Fraction(num * other.num,
                        den * other.den);
    }

    Fraction operator/(Fraction const& other) const {
        if (other.num == 0)
            throw std::invalid_argument("Division by zero fraction");
        return Fraction(num * other.den,
                        den * other.num);
    }

    Fraction operator+(long long x) const { return Fraction(num + x * den, den); }
    Fraction operator-(long long x) const { return Fraction(num - x * den, den); }
    Fraction operator*(long long x) const { return Fraction(num * x, den); }
    Fraction operator/(long long x) const {
        if (x == 0)
            throw std::invalid_argument("Division by zero integer");
        return Fraction(num, den * x);
    }

    
    Fraction& operator+=(Fraction const& other) { return *this = *this + other; }
    Fraction& operator-=(Fraction const& other) { return *this = *this - other; }
    Fraction& operator*=(Fraction const& other) { return *this = *this * other; }
    Fraction& operator/=(Fraction const& other) { return *this = *this / other; }

    Fraction& operator+=(long long x) { return *this = *this + x; }
    Fraction& operator-=(long long x) { return *this = *this - x; }
    Fraction& operator*=(long long x) { return *this = *this * x; }
    Fraction& operator/=(long long x) { return *this = *this / x; }

    // comparison
    bool operator==(Fraction const& other) const {
        return num == other.num && den == other.den;
    }

    bool operator<(Fraction const& other) const {
        return num * other.den < other.num * den;
    }

    bool operator!=(Fraction const& other) const { return !(*this == other); }
    bool operator>(Fraction const& other) const { return other < *this; }
    bool operator<=(Fraction const& other) const { return !(*this > other); }
    bool operator>=(Fraction const& other) const { return !(*this < other); }

    // Output stream
    friend std::ostream& operator<<(std::ostream& os, Fraction const& f) {
        if (f.den == 1) {
            return os << "(" << f.num << ")";
        }
        return os << "(" << f.num << "/" << f.den << ")";
    }
};
