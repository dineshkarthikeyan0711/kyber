#include <stdio.h>
#include "kem.h"

int main(void)
{
    // Generate key pair
    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    crypto_kem_keypair(pk, sk);

    // Create input message
    uint8_t input_message[] = "Hello, Kyber!";

    printf("Input Message: %s\n", input_message);

    // Perform key encapsulation
    uint8_t ct[CRYPTO_CIPHERTEXTBYTES];
    uint8_t ss[CRYPTO_BYTES];
    crypto_kem_enc(ct, ss, pk);

    // Perform key decapsulation
    uint8_t decrypted_ss[CRYPTO_BYTES];
    crypto_kem_dec(decrypted_ss, ct, sk);

    // Compare original shared secret with decrypted shared secret
    int success = 1;
    for (size_t i = 0; i < CRYPTO_BYTES; ++i) {
        if (ss[i] != decrypted_ss[i]) {
            success = 0;
            break;
        }
    }

    printf("Decrypted Shared Secret: ");
    for (size_t i = 0; i < CRYPTO_BYTES; ++i) {
        printf("%02x ", decrypted_ss[i]);
    }
    printf("\n");

    if (success) {
        printf("Experiment succeeded: Shared secrets match!\n");
    } else {
        printf("Experiment failed: Shared secrets do not match!\n");
    }

    return 0;
}