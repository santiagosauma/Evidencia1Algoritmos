class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._autocomplete(node, prefix)

    def _autocomplete(self, node, prefix):
        results = []
        if node.is_end_of_word:
            results.append(prefix)
        for char, next_node in node.children.items():
            results.extend(self._autocomplete(next_node, prefix + char))
        return results
