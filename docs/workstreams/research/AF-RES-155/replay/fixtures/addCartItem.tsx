export const addCartItem = (product: Product, quantity: number = 1) => async (dispatch: Dispatch, getState: () => RootState) => {
    const cartData = { product: product, quantity: quantity };

    try {
        dispatch(addCartItemRequest());
        await axiosInstance.post(CART_URI, cartData);
        dispatch(addCartItemSuccess(cartData));
        saveItemInStorage(CART_ITEMS, getState().cart.cartItems);
    } catch (error) {
        const err = error as ErrorResponse;
        dispatch(addCartItemFailed(throwErrorResponse(err)));
    }
};
