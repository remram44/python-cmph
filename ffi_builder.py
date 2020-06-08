import cffi
import textwrap


ffi_builder = cffi.FFI()
ffi_builder.set_source(
    'cmph._ffi',
    textwrap.dedent(r'''\
        #include <cmph.h>
        #include <string.h>

        #define QUOTE(x) #x

        int build_hash_brz(char *filename, char **keys, unsigned int nkeys) {
            cmph_t *hash;

            FILE *mphf_fd = fopen(filename, "w");
            if(mphf_fd == NULL) {
                return 1;
            }

            /* Source of keys */
            cmph_io_adapter_t *source = cmph_io_vector_adapter(keys, nkeys);

            /* Create minimal perfect hash function using the brz algorithm */
            cmph_config_t *config = cmph_config_new(source);
            cmph_config_set_algo(config, CMPH_BRZ);
            cmph_config_set_mphf_fd(config, mphf_fd);
            hash = cmph_new(config);
            cmph_config_destroy(config);
            cmph_dump(hash, mphf_fd);
            cmph_destroy(hash);
            fclose(mphf_fd);
            cmph_io_vector_adapter_destroy(source);

            return 0;
        }

        void *build_hash(char **keys, unsigned int nkeys, char *algo_name) {
            cmph_t *hash;
            CMPH_ALGO algo;

            if(strcmp(algo_name, "BMZ") == 0) algo = CMPH_BMZ;
            else if(strcmp(algo_name, "BMZ8") == 0) algo = CMPH_BMZ8;
            else if(strcmp(algo_name, "CHM") == 0) algo = CMPH_CHM;
            else if(strcmp(algo_name, "FCH") == 0) algo = CMPH_FCH;
            else if(strcmp(algo_name, "BDZ") == 0) algo = CMPH_BDZ;
            else if(strcmp(algo_name, "BDZ_PH") == 0) algo = CMPH_BDZ_PH;
            else if(strcmp(algo_name, "CHD_PH") == 0) algo = CMPH_CHD_PH;
            else if(strcmp(algo_name, "CHD") == 0) algo = CMPH_CHD;
            else {
                fprintf(
                    stderr,
                    "cmph: build_hash: invalid algo \"%s\"\n", algo_name
                );
                return NULL;
            }

            /* Source of keys */
            cmph_io_adapter_t *source = cmph_io_vector_adapter(keys, nkeys);

            /* Create minimal perfect hash function using the brz algorithm */
            cmph_config_t *config = cmph_config_new(source);
            cmph_config_set_algo(config, algo);
            hash = cmph_new(config);
            cmph_config_destroy(config);
            cmph_io_vector_adapter_destroy(source);

            return hash;
        }

        int dump_hash(void *mph, char *filename) {
            cmph_t *hash = mph;

            FILE *mphf_fd = fopen(filename, "w");
            if(mphf_fd == NULL) {
                return 1;
            }

            cmph_dump(hash, mphf_fd);
            fclose(mphf_fd);

            return 0;
        }

        void destroy_hash(void *mph) {
            cmph_t *hash = mph;
            cmph_destroy(hash);
        }

        void *load_hash(char *filename) {
            cmph_t *hash;
            FILE *mphf_fd = fopen(filename, "r");
            if(mphf_fd == NULL) {
                return NULL;
            }
            hash = cmph_load(mphf_fd);
            /*fclose(mphf_fd);*/
            return hash;
        }

        int find_key(void *mph, char *key) {
            unsigned int id = cmph_search(mph, key, (cmph_uint32)strlen(key));
            return id;
        }
    '''),
    libraries=['cmph'],
)
ffi_builder.cdef('''\
    int build_hash_brz(char *filename, char **keys, unsigned int nkeys);
    void *build_hash(char **keys, unsigned int nkeys, char *algo_name);
    int dump_hash(void *mph, char *filename);
    void *load_hash(char *filename);
    void destroy_hash(void *mph);
    int find_key(char *filename, char *key);
''')


if __name__ == '__main__':    # not when running with setuptools
    ffi_builder.compile(verbose=True)
