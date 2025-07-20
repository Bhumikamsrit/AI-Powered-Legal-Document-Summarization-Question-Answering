class Solution {
public:
    vector<string> wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> dict(wordDict.begin(), wordDict.end());
        
        // Early pruning: check if word break is possible
        if (!canWordBreak(s, dict)) {
            return {};
        }
        
        unordered_map<string, vector<string>> memo;
        return helper(s, dict, memo);
    }
    
private:
    // Check if word break is possible using DP (Word Break I)
    bool canWordBreak(const string& s, const unordered_set<string>& dict) {
        int n = s.length();
        vector<bool> dp(n + 1, false);
        dp[0] = true;
        
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && dict.count(s.substr(j, i - j))) {
                    dp[i] = true;
                    break;
                }
            }
        }
        
        return dp[n];
    }
    
    vector<string> helper(const string& s, const unordered_set<string>& dict, 
                         unordered_map<string, vector<string>>& memo) {
        // Check if already computed
        if (memo.count(s)) {
            return memo[s];
        }
        
        vector<string> result;
        
        // Base case: empty string
        if (s.empty()) {
            result.push_back("");
            return result;
        }
        
        // Try all possible prefixes
        for (int i = 1; i <= s.length(); i++) {
            string prefix = s.substr(0, i);
            if (dict.count(prefix)) {
                string suffix = s.substr(i);
                vector<string> suffixResults = helper(suffix, dict, memo);
                
                for (const string& suffixResult : suffixResults) {
                    if (suffixResult.empty()) {
                        result.push_back(prefix);
                    } else {
                        result.push_back(prefix + " " + suffixResult);
                    }
                }
            }
        }
        
        memo[s] = result;
        return result;
    }
};