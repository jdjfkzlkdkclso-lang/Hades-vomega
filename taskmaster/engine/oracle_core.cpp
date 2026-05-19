#include <iostream>
#include <vector>
#include <numeric>
#include <cmath>
#include <string>

struct Prediction {
    double next_val;
    double confidence;
};

Prediction calculate(const std::vector<double>& data) {
    size_t n = data.size();
    if (n < 2) return {0.0, 0.0};
    
    double x_sum = n * (n - 1) / 2.0;
    double y_sum = std::accumulate(data.begin(), data.end(), 0.0);
    double xy_sum = 0, x2_sum = 0;
    
    for(size_t i = 0; i < n; ++i) {
        xy_sum += i * data[i];
        x2_sum += i * i;
    }
    
    double slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum);
    double intercept = (y_sum - slope * x_sum) / n;
    
    // Simple R^2 para confianza
    double y_mean = y_sum / n;
    double ss_res = 0, ss_tot = 0;
    for(size_t i = 0; i < n; ++i) {
        double fit = slope * i + intercept;
        ss_res += std::pow(data[i] - fit, 2);
        ss_tot += std::pow(data[i] - y_mean, 2);
    }
    
    return { slope * n + intercept, 1.0 - (ss_res / (ss_tot + 1e-9)) };
}

int main() {
    std::string input;
    std::vector<double> series;
    while (std::cin >> input) {
        try { series.push_back(std::stod(input)); } catch(...) {}
    }
    Prediction res = calculate(series);
    std::cout << res.next_val << " " << res.confidence << std::endl;
    return 0;
}
