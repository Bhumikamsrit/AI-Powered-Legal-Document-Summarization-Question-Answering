class Solution {
public:
    vector<string> wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> dict(wordDict.begin(), wordDict.end());
        unordered_map<string, vector<string>> memo;
        return helper(s, dict, memo);
    }
    
private:
    vector<string> helper(const string& s, const unordered_set<string>& dict, 
                         unordered_map<string, vector<string>>& memo) {
        // Check if already computed
        if (memo.find(s) != memo.end()) {
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
            if (dict.find(prefix) != dict.end()) {
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