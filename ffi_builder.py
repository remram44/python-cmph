import cffi
import textwrap


ffi_builder = cffi.FFI()
ffi_builder.set_source(
    'cmph._ffi',
    textwrap.dedent(r'''\    
        #include <cmph.h>
        #include <string.h>
        
        int build_hash(char *filename, char **keys, unsigned int nkeys) {
            unsigned int i = 0;
            FILE *mphf_fd = fopen(filename, "w");
            /* Source of keys */
            cmph_io_adapter_t *source = cmph_io_vector_adapter(keys, nkeys);
    
            /* Create minimal perfect hash function using the brz algorithm */
            cmph_config_t *config = cmph_config_new(source);
            cmph_config_set_algo(config, CMPH_BRZ);
            cmph_config_set_mphf_fd(config, mphf_fd);
            cmph_t *hash = cmph_new(config);
            cmph_config_destroy(config);
            cmph_dump(hash, mphf_fd);
            cmph_destroy(hash);
            fclose(mphf_fd);
            cmph_io_vector_adapter_destroy(source);
            
            return 0;
        }
        
        int find_key(char *filename, char *key) {
            FILE *mphf_fd = fopen(filename, "r");
            cmph_t *hash = cmph_load(mphf_fd);
            
            unsigned int id = cmph_search(hash, key, (cmph_uint32)strlen(key));
            printf("key:%s -- hash:%u\n", key, id);
            
            cmph_destroy(hash);
            fclose(mphf_fd);
            
            return 0;
        }
    '''),
    libraries=['cmph'],
)
ffi_builder.cdef('''\
    int build_hash(char *filename, char **keys, unsigned int nkeys);
    int find_key(char *filename, char *key);
''')


if __name__ == '__main__':    # not when running with setuptools
    ffi_builder.compile(verbose=True)
